from dataclasses import asdict, dataclass

from flask_login import UserMixin
from flask_pymongo import ObjectId
from werkzeug.security import check_password_hash, generate_password_hash

from WeddingWebsite.extensions import mongo


@dataclass
class Guest(UserMixin):
    _id: ObjectId
    username: str
    _password: str
    name: str
    email: str
    roles: list = None
    party: list = None
    RSVP_status: list = None
    plus_one: list = None
    dietary_restrictions: list = None

    def __post_init__(self):
        # Sets password hash on user registration
        if "pbkdf2:sha256:" not in self._password:
            self._password = generate_password_hash(self._password)

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, val):
        self._password = generate_password_hash(val)

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, val):
        self._id = val

    def check_password(self, password):
        return check_password_hash(self._password, password)

    def __str__(self):
        return f"User {self.username}, with id: {self.id}"

    def add_to_mongodb(self, db):
        guests = db.guests
        guest_to_add = asdict(self)
        del guest_to_add["_id"]
        result = guests.insert_one(guest_to_add)
        self.id = result.inserted_id
        return result

    def update_db(self, db):
        result = db.guests.update_one({"_id": self.id}, {"$set": asdict(self)})
        if result.modified_count != 1:
            return False
        return True


class GuestCollection:
    def __init__(self):
        self.guests = [Guest(**x) for x in mongo.db.guests.find({})]

    def get_guest_by_id(self, _id):
        for guest in self.guests:
            if guest.id == ObjectId(_id):
                return guest
        return None

    def get_guest_by_username(self, username):
        for guest in self.guests:
            if guest.username == username:
                return guest
        return None

    def __len__(self):
        return len(self.guests)

    def __getitem__(self, index):
        return self.guests[index]

    def __str__(self):
        result = "Guests in collection:"
        for guest in self.guests:
            result += f"\n\t{guest}"
        return result
