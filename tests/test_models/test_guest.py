from werkzeug.security import check_password_hash

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
