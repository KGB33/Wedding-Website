from tests.conftest import log_in


def test_photos_view(test_client):
    log_in(test_client)
    response = test_client.get("/photos")
    assert response.status_code == 200
    assert b"<!-- photos.html -->" in response.data
