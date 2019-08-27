from tests.conftest import log_in


def test_requires_roles_with_valid_roles(new_guest, test_client, mongo_db):
    """
    GIVEN a Flask app
    WHEN a user attempts to access a restricted route that they HAVE the roles to access
    THEN Check that the user successfully accesses the route
    """
    new_guest.roles = ["test_role"]
    new_guest.add_to_mongodb(mongo_db)
    assert log_in("username", "password", test_client)
    response = test_client.get("/test_requires_roles")
    assert response.status_code == 200
    assert b"Access Granted" in response.data
