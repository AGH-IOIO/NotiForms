import os
from flaskr import app

if __name__ == '__main__':
    test = os.environ.get("TEST", "n")
    if test == "y":
        os.execlp("pytest", "-v")

    debug = os.environ.get("FLASK_DEBUG", False)
    app.run(host="0.0.0.0", port=8080, debug=debug)
