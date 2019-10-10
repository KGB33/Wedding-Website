from tests.conftest import log_in


def test_valid_login(test_client):
    """
    GIVEN a Flask App
    WHEN the '/login' page is posted (w/ valid data)
    THEN check if the response is valid
    """
    response = test_client.post(
        "/auth/login",
        data={"username": "t_default", "password": "123456"},
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert b"Logged in t_default successfully" in response.data
    assert b"<!-- Home.html -->" in response.data
    assert b'<link href="static/base.css"' in response.data


def test_invalid_login(test_client):
    """
    GIVEN a Flask App
    WHEN the '/login' page is posted (w/ invalid data)
    THEN check if the response is valid
    """
    response = test_client.post(
        "/auth/login",
        data={"username": "Wrong Username", "password": "Not The Password"},
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert b"Invalid username or password" in response.data
    assert b"Sign In" in response.data


def test_login_when_user_is_authenticated(test_client):
    """
    GIVEN a flask app
    WHEN the '/login' page is requested by an authenticated user
    THEN check that the user is redirected to '/' and a message is flashed
    """
    log_in(test_client, username="t_default", password="123456")
    response = test_client.post("/auth/login", follow_redirects=True)
    assert response.status_code == 200
    assert b"<!-- Home.html -->" in response.data
    assert b'<link href="static/base.css"' in response.data
    assert b"You are already logged in!" in response.data
