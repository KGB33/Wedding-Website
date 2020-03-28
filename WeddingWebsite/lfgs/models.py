from dataclasses import dataclass, asdict
from typing import Literal

from flask_pymongo import ObjectId

from WeddingWebsite.lfgs.exceptions import LFGIsFull


@dataclass
class LFG:
    owner_id: str
    owner_name: str
    members: dict  # {member_id: member_contact_info}
    _max_members: int
    info: str
    group_type: Literal["CARPOOL", "HOTEL"]
    _id: ObjectId = None

    def __post_init__(self):
        if self.total_members > self.max_members:
            raise ValueError(f"LFG has more members than allowed!")

    @property
    def max_members(self):
        return self._max_members

    @max_members.setter
    def max_members(self, value):
        if value < self.total_members:
            raise LFGIsFull(
                f"Cannot reduce total members to less than current memebers"
            )
        self._max_members = value

    @property
    def full(self):
        if self.total_members < self.max_members:
            return False
        return True

    @property
    def total_members(self):
        return 1 + len(self.members)  # Owner + Members

    def __str__(self):
        return f"LFG is owned by {self.owner_name} and has {self.total_members}/{self.max_members} members"

    def add_to_collection(self, collection):
        lfg_to_add = asdict(self)
        del lfg_to_add["_id"]
        result = collection.insert_one(lfg_to_add)
        self._id = result.inserted_id
        return result

    def update_collection(self, collection):
        result = collection.update_one({"_id": self._id}, {"$set": asdict(self)})
        if result.modified_count != 1:
            return False
        return True

    def add_member(self, member_id, member_name):
        if self.full:
            raise LFGIsFull(f"LFG Is Full, cannot add more members")
        self.members.update({member_id: member_name})

    def remove_member(self, member_id):
        del self.members[member_id]


class LFGCollection:
    def __init__(self, collection):
        self.lfgs = [LFG(**x) for x in collection.find({})]

    def get_lfg_by_id(self, _id):
        for lfg in self.lfgs:
            if lfg.id == ObjectId(_id):
                return lfg
        return None

    def get_lfg_by_username(self, username):
        for lfg in self.lfgs:
            if lfg.username == username:
                return lfg
        return None

    def __len__(self):
        return len(self.lfgs)

    def __getitem__(self, index):
        return self.lfgs[index]

    def __str__(self):
        result = "lfgs in collection:"
        for lfg in self.lfgs:
            result += f"\n\t{lfg}"
        return result
