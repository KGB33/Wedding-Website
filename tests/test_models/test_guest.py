from werkzeug.security import check_password_hash

from WeddingWebsite.models import Guest


"""
Tests for the Guest Model
"""


def test_init_guest(new_guest):
    """
    GIVEN a Guest Model
    WHEN a new Guest is created
    THEN check the id, username, password, name, email, roles and, party
    """
    assert new_guest.id == 0
    assert new_guest.username == "username_new"
    assert check_password_hash(new_guest.password, "password")
    assert new_guest.name == "name"
    assert new_guest.email == "email_new@email.com"
    assert new_guest.roles == ["roles"]
    assert new_guest.party == ["Parties"]


def test_guest_check_password_change(new_guest):
    """
    GIVEN a Guest model
    WHEN the password is changed
    THEN check that the password was hashed correctly
    """
    new_guest.password = "The new Password"
    assert new_guest.check_password("The new Password")
    assert new_guest.password != "The New Password"  # Not in plan text
    assert not new_guest.check_password("Not The Password")


def test_guest__str__(new_guest):
    """
    GIVEN a Guest model
    CHECK That the __str__ method acts as intended
    """
    assert f"User {new_guest.username}, with id: {new_guest.id}" == new_guest.__str__()


def test_update_db(mongo_db, new_guest):
    """
    GIVEN a guest, guest, in a database
    WHEN guest.update_db(db) is called
    THEN check that the guest is updated correctly
    """
    _id = new_guest.add_to_mongodb(mongo_db).inserted_id
    new_guest.username = "A new Username!!"
    new_guest.name = "A new Name!!"
    new_guest.update_db(mongo_db)
    guest_from_db = Guest(**mongo_db.guests.find_one({"_id": _id}))
    assert new_guest.username == guest_from_db.username
    assert new_guest.name == guest_from_db.name


def test_update_db_guest_not_in(mongo_db, new_guest):
    """
    GIVEN a database and a guest NOT in the database
    WHEN the guest updates the database
    THEN check that the database is not updated
    """
    new_guest.username = "A new Username!!"
    new_guest.name = "A new Name!!"
    assert not new_guest.update_db(mongo_db)
    assert mongo_db.guests.find_one({"username": "A new Username!!"}) is None
