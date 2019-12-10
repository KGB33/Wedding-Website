from flask_login import LoginManager
from flask_pymongo import PyMongo


# Create PyMongo DB
mongo = PyMongo()

# Create login manager
login_manager = LoginManager()

login_manager.refresh_view = 'auth.refresh_login'

