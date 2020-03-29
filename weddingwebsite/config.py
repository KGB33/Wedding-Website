import os


if not (FLASK_SECRET_KEY := os.getenv("FLASK_SECRET_KEY")):
    raise OSError("FLASK_SECRET_KEY not in .env")
if not (DB_USER := os.getenv("DB_USER")):
    raise OSError("DB_USER not in .env")
if not (DB_PASSWORD := os.getenv("DB_PASSWORD")):
    raise OSError("DB_PASSWORD not in .env")
if not (DB_NAME := os.getenv("DB_NAME")):
    raise OSError("DB_NAME not in .env")
if not (DB_NAMESPACE := os.getenv("DB_NAMESPACE")):
    raise OSError("DB_NAMESPACE not in .env")


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


class ProductionConfig(BaseConfig):
    MONGO_URI = f"mongodb+srv://{DB_USER}:{DB_PASSWORD}@{DB_NAME}-pylxy.mongodb.net/{DB_NAMESPACE}?retryWrites=true&w=majority"
