from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Blueprints import
from .handlers.user import users_bp

# Blueprints registration
app.register_blueprint(users_bp)
