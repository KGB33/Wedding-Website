import pytest

from tests.conftest import log_in
from weddingwebsite.auth.utils import requires_roles
from weddingwebsite.auth.exceptions import NoRolesProvided


def test_requires_roles_with_valid_roles(template_user, test_client, mongo_db):
    """
    GIVEN a Flask app
    WHEN a user attempts to access a restricted route that they HAVE the roles to access
    THEN Check that the user successfully accesses the route
    """
    template_user.roles = ["test_role"]
    template_user.add_to_collection(mongo_db.guests)
    log_in(test_client, username="t_template_user")
    response = test_client.get("/test_requires_roles")
    assert response.status_code == 200
    assert b"Access Granted" in response.data


def test_requires_roles_with_invalid_roles(template_user, test_client, mongo_db):
    """
    GIVEN a Flask app
    WHEN a user attempts to access a restricted route that they DO NOT HAVE the roles to access
    THEN Check that the user is redirected successfully to the unauthorized page
    """
    template_user.roles = ["test_role_fail"]
    template_user.add_to_collection(mongo_db.guests)
    log_in(test_client, username="t_template_user")
    response = test_client.get("/test_requires_roles", follow_redirects=True)
    assert response.status_code == 200
    assert b"you lack the required roles to view your requested page." in response.data


def test_requires_roles_with_anon_user(test_client):
    """
    GIVEN a flask app
    WHEN an anon user attempts to access a restricted route
    THEN Check that they are redirected to the login page
    """
    response = test_client.get("/test_requires_roles", follow_redirects=True)
    assert response.status_code == 200
    assert b"Sign In" in response.data


def test_requires_roles_no_roles_provided():
    """
    GIVEN a 'route' with the @requires_roles decorator, but provides no roles
    WHEN the 'route' is called
    THEN check that a readable error message is raised
    """

    @requires_roles()
    def a_method_for_testing():
        return True

    with pytest.raises(NoRolesProvided) as excinfo:
        a_method_for_testing()
    assert "No Roles provided, Please use @login_required instead" in str(excinfo.value)


def test_requires_roles_user_has_no_roles(test_client, template_user, mongo_db):
    """
    GIVEN a Flask app,
    WHEN a user with no roles attemps to access a route decorated with @roles_required
    THEN check that the user is redirected to the 'you don't have the required roles' page
    """
    template_user.roles = None
    template_user.add_to_collection(mongo_db.guests)
    log_in(test_client, username="t_template_user")
    response = test_client.get("/test_requires_roles", follow_redirects=True)
    assert response.status_code == 200
    assert (
        b"You are seeing this page because you lack the required roles to view your requested page."
        in response.data
    )
