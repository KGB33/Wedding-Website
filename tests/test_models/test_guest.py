from werkzeug.security import check_password_hash

from WeddingWebsite.models import Guest


"""
Tests for the User Model
"""

# Tools

# Used to instance an Guest object
g_dict = {
    "_id": 0,
    "username": "username",
    "_password": "password",
    "name": "name",
    "email": "email",
    "roles": ["roles"],
    "party": ["Parties"],
}


def test_init_guest_from_vals():
    g = Guest(0, "username", "password", "name", "email", ["roles"], ["Parties"])
    assert g._id == 0
    assert g.username == "username"
    assert check_password_hash(g._password, "password")
    assert g.name == "name"
    assert g.email == "email"
    assert g.roles == ["roles"]
    assert g.party == ["Parties"]


def test_init_guest_from_dict():
    g = Guest(**g_dict)
    assert g._id == 0
    assert g.username == "username"
    assert check_password_hash(g._password, "password")
    assert g.name == "name"
    assert g.email == "email"
    assert g.roles == ["roles"]
    assert g.party == ["Parties"]


def test_guest_password_property():
    g = Guest(**g_dict)
    assert check_password_hash(g._password, "password")
    assert check_password_hash(g.password, "password")
    g.password = "new_password"
    assert check_password_hash(g._password, "new_password")
    assert check_password_hash(g.password, "new_password")


def test_guest_id_property():
    g = Guest(**g_dict)
    assert g._id == g.id


def test_guest_check_password():
    g = Guest(**g_dict)
    assert g.check_password("password")
    assert not g.check_password("Not The Password")


def test_guest__str__():
    g = Guest(**g_dict)
    assert f"User {g.username}, with id: {g.id}" == g.__str__()
