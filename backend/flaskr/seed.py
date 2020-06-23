import os
from datetime import datetime, timedelta

from .database import connection
from .database.form_results_dao import FormResultsDAO
from .database.message_box_dao import MessageBoxDAO
from .database.pending_forms_dao import PendingFormsDAO
from .database.templates_dao import TemplateDAO
from .database.user_dao import UserDAO
from .model.forms import Template, Form
from .model.message_box import MessageBox
from .model.results import FormResults
from .model.user import User


def seed_forms():
    question1 = {
        "type": "single_choice",
        "title": "Czy jesteś na nie?",
        "choices": ["TAK", "NIE"],
        "answer": -1
    }
    question2 = {
        "type": "open_text",
        "title": "Napisz coś o sobie?",
        "answer": ""
    }
    question3 = {
        "type": "multiple_choice",
        "title": "Czy?",
        "choices": ["TAK", "NIE", "NIE WIEM"],
        "answer": []
    }

    template_data = {
        "owner": "team_owner",
        "title": "Referendum",
        "questions": [question1, question2, question3]
    }
    template = Template(template_data)
    template_dao = TemplateDAO()
    template_dao.insert_one(template)

    send_date = datetime.utcnow()
    # Simulate past-deadline form
    deadline = send_date - timedelta(days=1.0)

    form_title = "AAAAA"
    results = FormResults(template, form_title=form_title, recipients=["admin"])
    results_dao = FormResultsDAO()
    results_dao.insert_one(results)

    notification_details = [
        {
            "type": "online",
            "dead_period": 60,
            "before_deadline_frequency": 60,
            "after_deadline_frequency": 30,
            "notify_date": deadline
        },
        {
            "type": "push",
            "dead_period": 60,
            "before_deadline_frequency": 60,
            "after_deadline_frequency": 30,
            "notify_date": deadline
        }
    ]

    form_data = {
        "title": form_title,
        "recipient": "admin",
        "results_id": results.id,
        "template": template.data,
        "deadline": deadline,
        "notification_details": notification_details
    }
    form = Form(form_data)
    PendingFormsDAO().insert_one(form)


def seed_user():
    data = {
        "username": "admin",
        "password": "admin",
        "email": "stubmail@gmail.com",
        "teams": []
    }
    user = User(data)
    UserDAO().insert_one(user)

    message_box = MessageBox({
        "owner": data["username"],
        "messages": []
    })
    message_box_dao = MessageBoxDAO()
    message_box_dao.insert_one(message_box)


def seed_all():
    # Flush database
    connection.drop_database(os.environ["DB_NAME"])
    # Seed database with initial data.
    seed_user()
    seed_forms()
