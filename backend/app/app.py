import os
from flask import Flask, Response

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    """Return the index.html page"""
    return "Hello world!"


if __name__ == '__main__':
    host  = os.environ.get("FLASK_HOST", "0.0.0.0")
    port  = os.environ.get("FLASK_PORT", 80)
    debug = os.environ.get("FLASK_DEBUG", False)
    app.run(host=host, port=port, debug=debug)
