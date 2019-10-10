from tests.conftest import log_in


def test_registry(test_client):
    log_in(test_client)
    response = test_client.get("/registry")
    assert 200 == response.status_code
    assert b"<!-- registry.html -->" in response.data
