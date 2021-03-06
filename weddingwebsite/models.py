import random
from dataclasses import asdict, dataclass, field
from typing import Literal

from flask_login import UserMixin
from flask_pymongo import ObjectId
from werkzeug.security import check_password_hash, generate_password_hash

from WeddingWebsite.exceptions import TooManyMembersError


@dataclass
class Guest(UserMixin):
    _id: ObjectId
    username: str
    _password: str
    name: str
    email: str
    roles: list = field(default_factory=list)
    party: list = field(default_factory=list)
    RSVP_status: list = field(default_factory=list)
    plus_one: list = field(default_factory=list)
    dietary_restrictions: list = field(default_factory=list)

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

    def add_roles_from_code(self, code):
        """
        Adds roles based on a given code.
        Used during registration for Bridesmaids, Groomsmen, etc.
        """
        # Groomsman
        if "G" in code:
            i = code.index("G")
            try:
                val = int(code[i + 1 : i + 3])
                if val % 3 == 0:
                    self.roles.append("groomsman")
            except ValueError:
                pass

        # Bridesmaid
        if "B" in code:
            i = code.index("B")
            try:
                val = int(code[i + 1 : i + 3])
                if val % 5 == 0:
                    self.roles.append("bridesmaid")
            except ValueError:
                pass

        # Wedding Party
        if "W" in code:
            i = code.index("W")
            try:
                val = int(code[i + 1 : i + 3])
                if val % 13 == 0:
                    self.roles.append("wedding_party")
            except ValueError:
                pass

        # Cabin Stayer
        if "C" in code:
            i = code.index("C")
            try:
                val = int(code[i + 1 : i + 3])
                if val % 21 == 0:
                    self.roles.append("cabin_stayer")
            except ValueError:
                pass

    def __str__(self):
        return f"User {self.username}, with id: {self.id}"

    def add_to_collection(self, collection):
        guest_to_add = asdict(self)
        del guest_to_add["_id"]
        result = collection.insert_one(guest_to_add)
        self.id = result.inserted_id
        return result

    def update_collection(self, collection):
        result = collection.update_one({"_id": self.id}, {"$set": asdict(self)})
        if result.modified_count != 1:
            return False
        return True

    @staticmethod
    def create_code_from_roles(*roles):
        code = ""
        if "groomsman" in roles:
            code += "G"
            code += f"{3 * random.randint(4, 33)}"

        if "bridesmaid" in roles:
            code += "B"
            code += f"{5 * random.randint(2, 19)}"

        if "wedding_party" in roles:
            code += "W"
            code += f"{13 * random.randint(1, 7)}"

        if "cabin_stayer" in roles:
            code += "C"
            code += f"{21 * random.randint(1, 4)}"

        return code


class GuestCollection:
    def __init__(self, collection):
        self.guests = [Guest(**x) for x in collection.find({})]

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


@dataclass
class LFG:
    creator: str
    members: list
    max_mebers: int
    full: bool = False

    def __post_init__(self):
        if self.creator not in self.members:
            self.members.append(self.creator)

        self.check_full()

    @property
    def num_members(self):
        return len(self.members)

    def check_full(self):
        if self.max_mebers == self.num_members:
            self.full = True
            return True
        elif self.max_mebers < self.num_members:
            raise TooManyMembersError
        else:
            self.full = False
            return False

    def add_member(self, member_name):
        if self.num_members >= self.max_mebers:
            raise TooManyMembersError

        self.members.append(member_name)
        self.check_full()

    def remove_member(self, member_name):
        self.members.remove(member_name)

    def __str__(self):
        return f"{self.num_members}/{self.max_mebers}, Created By: {self.creator}, Members: {self.members}"


class Carpool(LFG):
    def __str__(self):
        return "Carpool: " * super().__str__()
