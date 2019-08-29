from tests.conftest import log_in


def test_requires_roles_with_valid_roles(new_guest, test_client, mongo_db):
    """
    GIVEN a Flask app
    WHEN a user attempts to access a restricted route that they HAVE the roles to access
    THEN Check that the user successfully accesses the route
    """
    new_guest.roles = ["test_role"]
    new_guest.add_to_mongodb(mongo_db)
    assert log_in(test_client, username="username_new")
    response = test_client.get("/test_requires_roles")
    assert response.status_code == 200
    assert b"Access Granted" in response.data


def test_requires_roles_with_invalid_roles(new_guest, test_client, mongo_db):
    """
    GIVEN a Flask app
    WHEN a user attempts to access a restricted route that they DO NOT HAVE the roles to access
    THEN Check that the user is redirected successfully to the unauthorized page
    """
    new_guest.roles = ["test_role_fail"]
    new_guest.add_to_mongodb(mongo_db)
    assert log_in(test_client, username="username_new")
    response = test_client.get("/test_requires_roles", follow_redirects=True)
    assert response.status_code == 200
    assert b"you lack the required roles to view your requested page." in response.data
