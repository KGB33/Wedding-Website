import pytest
from flaskr import create_app



@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    app = create_app({
        'MONGODB_SETTINGS': {'test': 'testing'},
        'TESTING': True,
        'CSRF_ENABLED': False,
    })

    yield app


@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()


@pytest.fixture
def runner(app):
    """A test runner for the app's Click commands."""
    return app.test_cli_runner()


class AuthActions(object):
    def __init__(self, client):
        self._client = client

    def login(self, username='test', password='test'):
        return self._client.post(
            '/auth/login',
            data={'username': username, 'password': password}
        )

    def logout(self):
        return self._client.get('/auth/logout')


@pytest.fixture
def auth(client):
    return AuthActions(client)
