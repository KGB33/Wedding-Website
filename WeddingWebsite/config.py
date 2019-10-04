from WeddingWebsite.secrets import DB_HOST, FLASK_SECRET_KEY


class BaseConfig:
    SECRET_KEY = FLASK_SECRET_KEY
    USER_APP_NAME = "Wedding-Website"  # Shown in and email templates and page footers
    USER_ENABLE_EMAIL = False  # Disable email authentication
    USER_ENABLE_USERNAME = True  # Enable username authentication
    USER_REQUIRE_RETYPE_PASSWORD = False  # Simplify register form


class TestingConfig(BaseConfig):
    TESTING = True
    WTF_CSRF_ENABLED = False
    MONGO_URI = "mongodb://127.0.0.1:27017/test"


class DevelopmentConfig(BaseConfig):
    MONGO_URI = DB_HOST
