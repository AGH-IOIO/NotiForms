import os
from flaskr import app

if __name__ == '__main__':
    if os.environ.get("TEST") == "y":
        os.execlp("pytest", "-v")
        
    debug = os.environ.get("FLASK_DEBUG", False)

    if os.environ.get("SEED") == "y":
        from flaskr.seed import seed_all
        seed_all()

    app.run(host="0.0.0.0", port=8080, debug=debug)
