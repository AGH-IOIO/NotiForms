from .database.user_dao import UserDAO
from .database.templates_dao import TemplateDAO
from .database.form_results_dao import FormResultsDAO
from .database.pending_forms_dao import PendingFormsDAO
from .model.user import User
from .model.forms import Template, Form
from .model.results import FormResults
from .database import connection

from datetime import datetime, timedelta

import os

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
    deadline = send_date + timedelta(days=1.0)

    results = FormResults(template, recipients=["admin"])
    results_dao = FormResultsDAO()
    results_dao.insert_one(results)

    form_data = {
        "title": "AAAAA",
        "recipient": "stubUser",
        "results_id": results.id,
        "template": template.data,
        "deadline": deadline
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

def seed_all():
    # Flush database
    connection.drop_database(os.environ["DB_NAME"])
    # Seed database with initial data.
    seed_user()
    seed_forms()
