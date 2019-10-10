from tests.conftest import log_in


def test_index(test_client):
    """
    GIVEN a Flask Application
    WHEN the '/' page is requested
    THEN check if the response is valid
    """
    response = test_client.get("/")
    assert response.status_code == 200
    assert b"<!-- index.html -->" in response.data


def test_index_logged_in(test_client):
    """
    GIVEN a Flask App
    WHEN the '/' page is requested, and a user is logged in
    THEN check that the response is personalized
    """
    log_in(test_client)
    response = test_client.get("/", follow_redirects=True)
    assert response.status_code == 200
    assert b"<!-- Home.html -->" in response.data
