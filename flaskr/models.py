from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash
from flask_pymongo import ObjectId
from dataclasses import dataclass


@dataclass
class Guest(UserMixin):
    _id: ObjectId
    username: str
    _password: str
    name: str
    email: str
    roles: list = None
    party: list = None

    def __post_init__(self):
        # Sets password hash on creation
        self._password = generate_password_hash(self._password)

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, password):
        self._password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self._password, password)

    def __str__(self):
        return f'{self.name} has roles: {self.roles} and is in party: {self.party}'

    def add_to_mongodb(self, db):
        guests = db.guests
        guests.insert_one({
            'username': self.username,
            '_password': self._password,
            'name': self.name,
            'email': self.email,
            'roles': self.roles,
            'party': self.party,
        })


