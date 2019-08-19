from flask_user import UserManager, UserMixin
from flaskr import app, db
from flask_mongoengine import MongoEngine


class Guest(db.Document, UserMixin):
    active = db.BooleanField(default=True)

    # User authentication information
    username = db.StringField(default='')
    password = db.StringField()

    # User information
    first_name = db.StringField(default='')
    last_name = db.StringField(default='')

    # Relationships
    roles = db.ListField(db.StringField(), default=[])
    party = db.StringField()

    def add_role(self, role):
        """
        Adds the role to the Guest's Roles
        :param role: role to be added
        """
        self.roles.append(role)

    def add_party(self, party):
        """
        Adds the relationship between a guest and a Party
        :param party: Party to add
        """
        self.party = party


user_manager = UserManager(app, db, Guest)
