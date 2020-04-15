from threading import Thread
from flask import current_app, render_template
from flask_mail import Message
from . import mail
import os


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(to, subject, template, **kwargs):
    app = current_app._get_current_object()
    msg = Message(os.environ['MAIL_SUBJECT_PREFIX'] + ' ' + subject,
                  sender=os.environ['MAIL_SENDER'],
                  recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)

    thread = Thread(target=send_async_email, args=[app, msg])
    thread.start()
    return thread
