import os
from flaskr import app

if __name__ == '__main__':
    if os.environ.get("TEST", None) == "y":
        os.execlp("pytest", "-v")
        
    debug = os.environ.get("FLASK_DEBUG", False)
    app.run(host="0.0.0.0", port=8080, debug=debug)
