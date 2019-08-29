def test_index(test_client):
    """
    GIVEN a Flask Application
    WHEN the '/' page is requested
    THEN check if the response is valid
    """
    response = test_client.get("/")
    assert response.status_code == 200
    assert b"Home Page" in response.data
    assert b"Hi !" in response.data


def test_index_logged_in(test_client, new_guest, mongo_db):
    """
    GIVEN a Flask App
    WHEN the '/' page is requested, and a user is logged in
    THEN check that the response is personalized
    """
    new_guest.add_to_mongodb(mongo_db)
    test_client.post(
        "/auth/login",
        data={"username": "username", "password": "password"},
        follow_redirects=True,
    )
    response = test_client.get("/", follow_redirects=True)
    assert response.status_code == 200
    assert b"<!-- Home.html -->" in response.data
    assert b'<link href="static/base.css"' in response.data
