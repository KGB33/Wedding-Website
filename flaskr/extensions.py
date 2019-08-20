from flask_pymongo import PyMongo
from flask_login import LoginManager

# Create PyMongo DB
mongo = PyMongo()

# Create login manager
lm = LoginManager()

