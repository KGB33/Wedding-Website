from tests.conftest import log_in


def test_valid_login(test_client, new_guest, mongo_db):
    """
    GIVEN a Flask App
    WHEN the '/login' page is posted (w/ valid data)
    THEN check if the response is valid
    """
    new_guest.add_to_mongodb(mongo_db)
    response = test_client.post(
        "/auth/login",
        data={"username": "username", "password": "password"},
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert b"Home Page" in response.data
    assert b"Hi username!" in response.data


def test_invalid_login(test_client, new_guest, mongo_db):
    """
    GIVEN a Flask App
    WHEN the '/login' page is posted (w/ invalid data)
    THEN check if the response is valid
    """
    new_guest.add_to_mongodb(mongo_db)
    response = test_client.post(
        "/auth/login",
        data={"username": "Wrong Username", "password": "Not The Password"},
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert b"Invalid username or password" in response.data
    assert b"Sign In" in response.data


def test_login_when_user_is_authenticated(new_guest, test_client, mongo_db):
    """
    GIVEN a flask app
    WHEN the '/login' page is requested by an authenticated user
    THEN check that the user is redirected to '/' and a message is flashed
    """
    new_guest.add_to_mongodb(mongo_db)
    log_in("username", "password", test_client)
    response = test_client.post("/auth/login", follow_redirects=True)
    assert response.status_code == 200
    assert b"Home Page" in response.data
    assert b"Hi username!" in response.data
    assert b"You are already logged in!" in response.data
