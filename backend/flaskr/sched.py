from flask_apscheduler import APScheduler
scheduler = APScheduler()
scheduler.api_enabled = True


# interval examples
@scheduler.task("interval", id="email_notifications", seconds=3)
def email_notifications():
    from .database.pending_forms_dao import PendingFormsDAO
    from .database.form_results_dao import FormResultsDAO

    pending_dao = PendingFormsDAO()
    results_dao = FormResultsDAO()

    pending = pending_dao.find({})

    print(len(pending), flush=True)
    for p in pending:
        r = results_dao.find_one_by_id(p.results_id)
        print(p, flush=True)
        print("----", flush=True)
        print(r, flush=True)
