from tests.conftest import log_in


def test_logout_auth_user(test_client, mongo_db):
    """
    GIVEN a flask app
    WHEN an authorized user logs out
    THEN check that the user was logged out successfully
    """
    assert log_in(test_client)
    response = test_client.get("auth/logout", follow_redirects=True)
    assert response.status_code == 200
    assert b"Hi !" in response.data
    assert b"You have been logged out." in response.data


def test_logout_anon_user(test_client):
    """
    GIVEN a flask app
    WHEN an anon user attemps to log out
    THEN check that a message flashes informing them that they are already logged out.
    """
    response = test_client.get("auth/logout", follow_redirects=True)
    assert response.status_code == 200
    assert b"Hi !" in response.data
    assert b"You were not, and still are not, logged in." in response.data