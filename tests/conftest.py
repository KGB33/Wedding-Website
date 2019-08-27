import pytest

from WeddingWebsite import create_app
from WeddingWebsite.auth import requires_roles
from WeddingWebsite.models import Guest


@pytest.fixture
def new_guest():
    g_dict = {
        "_id": 0,
        "username": "username",
        "_password": "password",
        "name": "name",
        "email": "email@email.com",
        "roles": ["roles"],
        "party": ["Parties"],
    }
    return Guest(**g_dict)


@pytest.fixture(scope="module")
def test_client():
    flask_app = create_app(test_config="../tests/flask_test_config.py")

    # Routes for testing Requires Roles
    @flask_app.route("/test_requires_roles")
    @requires_roles("test_role")
    def test_requires_roles():
        return "Access Granted"

    testing_client = flask_app.test_client()
    ctx = flask_app.app_context()
    ctx.push()

    yield testing_client

    ctx.pop()


@pytest.fixture
def mongo_db():
    from WeddingWebsite.extensions import mongo

    yield mongo.db

    mongo.db.drop_collection("guests")


def log_in(username, password, app):
    response = app.post(
        "/auth/login",
        data={"username": username, "password": password},
        follow_redirects=True,
    )
    if response.status_code == 200:
        return True
    return False
