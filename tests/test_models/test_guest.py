import pytest
from werkzeug.security import check_password_hash

from WeddingWebsite.models import Guest


"""
Tests for the Guest Model
"""


@pytest.mark.no_mongo_db
def test_init_guest(template_user):
    """
    GIVEN a Guest Model
    WHEN a new Guest is created
    THEN check the id, username, password, name, email, roles and, party
    """
    assert template_user.id == 0
    assert template_user.username == "t_template_user"
    assert check_password_hash(template_user.password, "123456")
    assert template_user.name == "t_template_user"
    assert template_user.email == "t_template_user@test.org"
    assert template_user.roles is None
    assert template_user.party is None


@pytest.mark.no_mongo_db
@pytest.mark.no_mock_hashlib_pbkdf2
def test_guest_check_password_change(template_user):
    """
    GIVEN a Guest model
    WHEN the password is changed
    THEN check that the password was hashed correctly
    """
    template_user.password = "The new Password"
    assert template_user.check_password("The new Password")
    assert template_user.password != "The New Password"  # Not in plan text
    assert not template_user.check_password("Not The Password")


@pytest.mark.no_mongo_db
def test_guest__str__(template_user):
    """
    GIVEN a Guest model
    CHECK That the __str__ method acts as intended
    """
    assert (
        f"User {template_user.username}, with id: {template_user.id}"
        == template_user.__str__()
    )


def test_update_db(mongo_db, template_user):
    """
    GIVEN a guest, guest, in a database
    WHEN guest.update_db(db) is called
    THEN check that the guest is updated correctly
    """
    _id = template_user.add_to_mongodb(mongo_db).inserted_id
    template_user.username = "A new Username!!"
    template_user.name = "A new Name!!"
    template_user.update_db(mongo_db)
    guest_from_db = Guest(**mongo_db.guests.find_one({"_id": _id}))
    assert template_user.username == guest_from_db.username
    assert template_user.name == guest_from_db.name


def test_update_db_guest_not_in(mongo_db, template_user):
    """
    GIVEN a database and a guest NOT in the database
    WHEN the guest updates the database
    THEN check that the database is not updated
    """
    template_user.username = "A new Username!!"
    template_user.name = "A new Name!!"
    assert not template_user.update_db(mongo_db)
    assert mongo_db.guests.find_one({"username": "A new Username!!"}) is None
