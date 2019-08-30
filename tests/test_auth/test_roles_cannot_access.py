import pytest

from tests.conftest import log_in
from WeddingWebsite.auth import roles_cannot_access
from WeddingWebsite.exceptions import NoRolesProvided


def test_roles_cannot_access_valid(new_guest, test_client, mongo_db):
    """
    GIVEN a flask app
    WHEN a user attempts to access a route that they don't have a role that cannot access
    THEN check that they are redirected to the restricted
    """
    new_guest.roles = ["any role under the sun"]
    new_guest.add_to_mongodb(mongo_db)
    assert log_in(test_client, username="username_new")
    response = test_client.get("/test_roles_cannot_access")
    assert response.status_code == 200
    assert b"Access Granted" in response.data


def test_roles_cannot_access_invalid(new_guest, test_client, mongo_db):
    """
    GIVEN a flask app
    WHEN a user attempts to access a route that they have a role that cannot access
    THEN check that they are redirected to the 'You don't have the roles' page
    """
    new_guest.roles = ["test_role_cannot_access"]
    new_guest.add_to_mongodb(mongo_db)
    assert log_in(test_client, username="username_new")
    response = test_client.get("/test_roles_cannot_access", follow_redirects=True)
    assert response.status_code == 200
    assert b"you lack the required roles to view your requested page." in response.data


def test_roles_cannot_access_with_anon_user(test_client):
    """
    GIVEN a flask app
    WHEN an anon user attempts to access a restricted route
    THEN Check that they are redirected to the login page
    """
    response = test_client.get("/test_roles_cannot_access", follow_redirects=True)
    assert response.status_code == 200
    assert b"Sign In" in response.data


def test_roles_cannot_access_no_roles_provided():
    """
    GIVEN a Flask app,
    WHEN a the developer adds a route with the @roles_cannot_access decorator, but provides no roles
    THEN check that a readable error message is raised
    """

    @roles_cannot_access()
    def a_method_for_testing():
        return True

    with pytest.raises(NoRolesProvided) as excinfo:
        a_method_for_testing()
    assert "No Roles provided, Please use @login_required instead" in str(excinfo.value)


def test_roles_cannot_access_user_has_no_roles(test_client, new_guest, mongo_db):
    """
    GIVEN a Flask app,
    WHEN a user with no roles attemps to access a route decorated with @roles_required
    THEN check that the user is redirected to the restricted page
    """
    new_guest.roles = None
    new_guest.add_to_mongodb(mongo_db)
    log_in(test_client, username="username_new")
    response = test_client.get("/test_roles_cannot_access", follow_redirects=True)
    assert response.status_code == 200
    assert b"Access Granted" in response.data
