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
    assert template_user.password == "123456"
    assert template_user.name == "t_template_user"
    assert template_user.email == "t_template_user@test.org"
    assert template_user.roles == []
    assert template_user.party == []


@pytest.mark.no_mongo_db
@pytest.mark.no_mock_password_hash
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
    WHEN guest.update_collection(db) is called
    THEN check that the guest is updated correctly
    """
    _id = template_user.add_to_collection(mongo_db.guests).inserted_id
    template_user.username = "A new Username!!"
    template_user.name = "A new Name!!"
    template_user.update_collection(mongo_db.guests)
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
    assert not template_user.update_collection(mongo_db.guests)
    assert mongo_db.guests.find_one({"username": "A new Username!!"}) is None


class TestAddRolesFromCode:
    def test_groomsman_code(self, template_user):
        """
        GIVEN a Guest
        WHEN add_roles_from_code is called with a valid groomsman code
        THEN check that the groomsman role was added
        """
        template_user.add_roles_from_code("G33")
        assert template_user.roles == ["groomsman"]

    def test_bridesmaid_code(self, template_user):
        """
        GIVEN a Guest
        WHEN add_roles_from_code is called with a valid bridesmaid code
        THEN check that the bridesmaid role was added
        """
        template_user.add_roles_from_code("B75")
        assert template_user.roles == ["bridesmaid"]

    def test_wedding_party_code(self, template_user):
        """
        GIVEN a Guest
        WHEN add_roles_from_code is called with a valid wedding_party code
        THEN check that the wedding_party role was added
        """
        template_user.add_roles_from_code("W26")
        assert template_user.roles == ["wedding_party"]

    def test_cabin_stayer_code(self, template_user):
        """
        GIVEN a Guest
        WHEN add_roles_from_code is called with a valid cabin_stayer code
        THEN check that the cabin_stayer role was added
        """
        template_user.add_roles_from_code("C42")
        assert template_user.roles == ["cabin_stayer"]

    def test_all_codes_in_one(self, template_user):
        """
        GIVEN a Guest
        WHEN add_roles_from_code is called with a code that contains valid parts for all the roles
        CHECK that all the roles are added
        """
        template_user.add_roles_from_code("G33B50W39C21")
        assert template_user.roles == [
            "groomsman",
            "bridesmaid",
            "wedding_party",
            "cabin_stayer",
        ]


class TestCreateCodeFromRoles:
    def test_no_role(self):
        """
        GIVEN a Guest
        WHEN create_code_from_roles is called with no role
        THEN check that it creates a code with no roles
        """
        assert Guest.create_code_from_roles() == ""

    def test_groomsman_role(self, template_user):
        """
        GIVEN a Guest
        WHEN create_code_from_roles is called with a valid groomsman role
        THEN check that the groomsman role is in the code
        """
        code = Guest.create_code_from_roles("groomsman")
        assert "G" in code
        i = code.index("G")
        val = int(code[i + 1 : i + 3])
        assert val % 3 == 0

        template_user.add_roles_from_code(code)
        assert template_user.roles == ["groomsman"]

    def test_bridesmaid_role(self, template_user):
        """
        GIVEN a Guest
        WHEN create_code_from_roles is called with a valid bridesmaid role
        THEN check that the bridesmaid role is in the code
        """
        code = Guest.create_code_from_roles("bridesmaid")
        assert "B" in code
        i = code.index("B")
        val = int(code[i + 1 : i + 3])
        assert val % 5 == 0

        template_user.add_roles_from_code(code)
        assert template_user.roles == ["bridesmaid"]

    def test_wedding_party_role(self, template_user):
        """
        GIVEN a Guest
        WHEN create_code_from_roles is called with a valid wedding_party role
        THEN check that the wedding_party role is in the code
        """
        code = Guest.create_code_from_roles("wedding_party")
        assert "W" in code
        i = code.index("W")
        val = int(code[i + 1 : i + 3])
        assert val % 13 == 0

        template_user.add_roles_from_code(code)
        assert template_user.roles == ["wedding_party"]

    def test_cabin_stayer_role(self, template_user):
        """
        GIVEN a Guest
        WHEN create_code_from_roles is called with a valid cabin_stayer role
        THEN check that the cabin_stayer role is in the code
        """
        code = Guest.create_code_from_roles("cabin_stayer")
        assert "C" in code
        i = code.index("C")
        val = int(code[i + 1 : i + 3])
        assert val % 21 == 0

        template_user.add_roles_from_code(code)
        assert template_user.roles == ["cabin_stayer"]

    def test_all_roles_in_one(self, template_user):
        """
        GIVEN a Guest
        WHEN create_code_from_roles is called with a role that contains valid parts for all the roles
        CHECK that all the roles are added
        """
        code = Guest.create_code_from_roles(
            *["groomsman", "bridesmaid", "wedding_party", "cabin_stayer"]
        )
        # Groomsman
        assert "G" in code
        i = code.index("G")
        val = int(code[i + 1 : i + 3])
        assert val % 3 == 0

        # Bridesmaid
        assert "B" in code
        i = code.index("B")
        val = int(code[i + 1 : i + 3])
        assert val % 5 == 0

        # Wedding Party
        assert "W" in code
        i = code.index("W")
        val = int(code[i + 1 : i + 3])
        assert val % 13 == 0

        # Cabin Stayer
        assert "C" in code
        i = code.index("C")
        val = int(code[i + 1 : i + 3])
        assert val % 21 == 0

        template_user.add_roles_from_code(code)
        assert template_user.roles == [
            "groomsman",
            "bridesmaid",
            "wedding_party",
            "cabin_stayer",
        ]
