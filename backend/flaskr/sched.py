from datetime import datetime, timedelta
from os import getenv
from random import choice

from flask_apscheduler import APScheduler

scheduler = APScheduler()
scheduler.api_enabled = True


@scheduler.task("interval", id="check_deadlines", seconds=int(getenv("CHECK_DEADLINES_INTERVAL", 10)))
def check_deadlines():
    from .database.form_results_dao import FormResultsDAO

    form_results_dao = FormResultsDAO()

    def handle(form_results):
        """
        This function checks if deadline for given form has passed and if so updates finished field in database
        """
        now = datetime.utcnow()
        deadline = form_results.deadline

        if deadline is not None and now >= deadline:
            form_results_dao.update_one_by_id(form_results.id, {"$set": {"finished": True}})
            print("{} marked as finished".format(form_results.title))

    all_results = form_results_dao.find({"finished": False})
    [handle(results) for results in all_results]


@scheduler.task("interval", id="email_notifications", seconds=5)
def email_notifications():
    TEMPLATE_NAME = "notification_email"
    THREATS = [
        "If you want to avoid trouble, you'd better fill it.",
        "If you won't fill it, there're gonna be concequences.",
        "There's gonna be trouble if you won't fill it.",
        "If you're considering not filling the form, you better think again. We know your IP address."
    ]

    from .database.pending_forms_dao import PendingFormsDAO
    from .database.user_dao import UserDAO
    from .email import send_email

    def handle(form):
        """
        This functions decides whether to send or not to send notification for given Form.
        """
        notification_details = form.notification_details
        email_details = next((x for x in notification_details if x.type == "e-mail"), None)
        if email_details is None:
            return

        now = datetime.utcnow()
        last_notify = email_details.notify_date

        if last_notify == form.send_date:
            notify_seconds = email_details.dead_period
        elif now <= form.deadline:
            notify_seconds = email_details.before_deadline_frequency
        else:
            notify_seconds = email_details.after_deadline_frequency

        notify_period = timedelta(seconds=notify_seconds)

        # By default don't send notification.
        send = now > last_notify + notify_period

        if not send:
            return

        # Generate email template data.
        template_data = {
            "username": form.recipient,
            "deadline": str(form.deadline),
            "threat": "" if last_notify == form.send_date else choice(THREATS)
        }

        # Find user email address
        target = UserDAO().find_one({"username": form.recipient})
        if target is None:
            print("Unable to send notification to %s." % form.recipient, flush=True)
            return

        email_addr = target.email
        send_email(email_addr, "[NotiForms] Pending '%s'" % form.title, TEMPLATE_NAME, **template_data)
        print("Notification for %s sent." % form.title, flush=True)
        PendingFormsDAO().update_one({"_id": form.id, "notification_details.type": "e-mail"},
                                     {"$set": {"notification_details.$.notify_date": now}})

    forms = PendingFormsDAO().find({})
    [handle(form) for form in forms]
