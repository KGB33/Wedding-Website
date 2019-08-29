def test_home_unauthorized_user(test_client):
    """
    GIVEN a flask app
    WHEN an unauthorized user gets '/home'
    THEN check that they are redirected to the sign in page
    """
    response = test_client.get("/home", follow_redirects=True)
    assert response.status_code == 200
    assert b"Sign In" in response.data
    assert b"New User?" in response.data


def test_home_authorized_user(test_client):
    """
    GIVEN a flask app
    WHEN an unauthorized user gets '/home'
    THEN check that they are redirected to the sign in page
    """
    test_client.post(
        "/auth/login",
        data={"username": "username", "password": "password"},
        follow_redirects=True,
    )
    response = test_client.get("/home", follow_redirects=True)
    assert response.status_code == 200
    assert b"<!-- Home.html -->" in response.data
    assert b'<link href="static/base.css"' in response.data
