from tests.conftest import log_in


def test_roles_cannot_access_valid(new_guest, test_client, mongo_db):
    new_guest.roles = ["any role under the sun"]
    new_guest.add_to_mongodb(mongo_db)
    assert log_in(test_client, username="username_new")
    response = test_client.get("/test_roles_cannot_access")
    assert response.status_code == 200
    assert b"Access Granted" in response.data


def test_roles_cannot_access_invalid(new_guest, test_client, mongo_db):
    new_guest.roles = ["test_role_cannot_access"]
    new_guest.add_to_mongodb(mongo_db)
    assert log_in(test_client, username="username_new")
    response = test_client.get("/test_roles_cannot_access", follow_redirects=True)
    assert response.status_code == 200
    assert b"you lack the required roles to view your requested page." in response.data
