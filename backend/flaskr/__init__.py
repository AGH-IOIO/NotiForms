from flask import Flask

app = Flask(__name__)

# Blueprints import
from flaskr.users import bp as users_bp

# Blueprints registration
app.register_blueprint(users_bp)
