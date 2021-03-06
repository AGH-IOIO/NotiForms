from bson import ObjectId
from datetime import datetime, date
from flask import Flask
from flask.json import JSONEncoder, JSONDecoder
from flask_cors import CORS
from flask_mail import Mail
from .sched import scheduler
import os


# custom MongoBD encoder and decoder for entire app
class MongoJSONEncoder(JSONEncoder):
    def default(self, o):
        # uses ISO format: YYYY-MM-DD, e. g. "2002-12-04"
        if isinstance(o, date):
            return str(date)

        # uses modified ISO format: YYYY-MM-DD HH-MM-SS
        # e. g. "2002-12-04 12:00:01"
        if isinstance(o, datetime):
            return o.strftime("%Y-%m-%d %H-%M-%S")

        if isinstance(o, ObjectId):
            return str(o)
        else:
            return super().default(o)


class MongoJSONDecoder(JSONDecoder):
    # uses the same formats as encoder
    def default(self, o):
        pass


app = Flask(__name__)

# Allow Cross-Origin requests.
CORS(app)

# Store JSON encoder
app.json_encoder = MongoJSONEncoder

# APScheduler config
if os.environ.get("WERKZEUG_RUN_MAIN") == "true":
    scheduler.init_app(app)
    scheduler.start()

# Mail config
app.config["MAIL_SERVER"] = os.environ["MAIL_SERVER"]
app.config["MAIL_PORT"] = int(os.environ["MAIL_PORT"])
app.config["MAIL_USE_TLS"] = os.environ.get("MAIL_USE_TLS", "true").lower() in ["true", "on", "1"]
app.config["MAIL_USERNAME"] = os.environ["MAIL_USERNAME"]
app.config["MAIL_PASSWORD"] = os.environ["MAIL_PASSWORD"]
mail = Mail(app)

# Blueprints import
from .handlers.user_handler import users_bp
from .handlers.team_handler import team_bp
from .handlers.template_handler import template_bp
from .handlers.form_handler import form_bp
from .handlers.message_handler import message_box_bp
from .handlers.push_handler import push_bp

# Blueprints registration
app.register_blueprint(users_bp)
app.register_blueprint(team_bp)
app.register_blueprint(template_bp)
app.register_blueprint(form_bp)
app.register_blueprint(message_box_bp)
app.register_blueprint(push_bp)
