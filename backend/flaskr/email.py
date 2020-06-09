from threading import Thread
from flask import current_app, render_template
from flask_mail import Message
from . import mail, app
import os


def send_async_email(to, subject, template, kwargs):
    with app.app_context():
        msg = Message(os.environ['MAIL_SUBJECT_PREFIX'] + ' ' + subject,
                      sender=os.environ['MAIL_SENDER'],
                      recipients=[to])

        msg.body = render_template(template + '.txt', **kwargs)
        msg.html = render_template(template + '.html', **kwargs)
        mail.send(msg)

def send_email(to, subject, template, **kwargs):
    thread = Thread(target=send_async_email, args=[to, subject, template, kwargs])
    thread.start()
    return thread
