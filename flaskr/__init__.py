from flask import Flask
from flaskr.secrets import DB_HOST, DB_NAME, FLASK_SECRET_KEY
from flask_mongoengine import MongoEngine
import os


def create_app(test_config=None):
    """ Flask application factory """

    # Setup Flask and load app.config
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=FLASK_SECRET_KEY,
        MONGODB_SETTINGS={
            'db': DB_NAME,
            'host': DB_HOST
        },
        USER_APP_NAME="Wedding-Website",  # Shown in and email templates and page footers
        USER_ENABLE_EMAIL=False,  # Disable email authentication
        USER_ENABLE_USERNAME=True,  # Enable username authentication
        USER_REQUIRE_RETYPE_PASSWORD=False,  # Simplify register form
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    return app


# Create app
app = create_app()


# Setup Flask-MongoEngine
db = MongoEngine(app)
