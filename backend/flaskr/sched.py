from flask_apscheduler import APScheduler
scheduler = APScheduler()
scheduler.api_enabled = True

from datetime import datetime, timedelta
from random import choice


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
        '''
        This functions decides whether to send or not to send notification for given Form.
        '''
        now = datetime.utcnow()
        notify_seconds = 60 if form.notify_period is None else form.notify_period
        notify_period = timedelta(seconds=notify_seconds)

        # By default don't send notification.
        send = False
        # Send first notification.
        send = send or form.last_notify is None
        # After exceeding the deadline, start sending periodic notifications.
        send = send or (now > form.deadline and now > form.last_notify + notify_period)

        if not send:
            return

        # Generate email template data.
        template_data = {
            "username": form.recipient,
            "deadline": str(form.deadline),
            "threat":  "" if form.last_notify is None else choice(THREATS)
        }

        # Find user email address
        target = UserDAO().find_one({"username": form.recipient})
        if target is None:
            print("Unable to send notification to %s." % form.recipient, flush=True)
            return

        email_addr = target.email
        send_email(email_addr, "[NotiForms] Pending '%s'" % form.title, TEMPLATE_NAME, **template_data)
        print("Notification for %s sent." % form.title, flush=True)
        PendingFormsDAO().update_one({"_id": form.id}, {"$set": {"last_notify": now}})


    forms = PendingFormsDAO().find({})
    [handle(form) for form in forms]


