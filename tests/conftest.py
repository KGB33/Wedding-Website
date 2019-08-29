import pytest

from WeddingWebsite import create_app
from WeddingWebsite.auth import requires_roles, roles_cannot_access
from WeddingWebsite.models import Guest


@pytest.fixture
def new_guest():
    g_dict = {
        "_id": 0,
        "username": "username_new",
        "_password": "password",
        "name": "name",
        "email": "email_new@email.com",
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

    # Routes for testing roles cannot access
    @flask_app.route("/test_roles_cannot_access")
    @roles_cannot_access("test_role_cannot_access")
    def test_roles_cannot_access():
        return "Access Granted"

    testing_client = flask_app.test_client()
    ctx = flask_app.app_context()
    ctx.push()

    yield testing_client

    ctx.pop()


@pytest.fixture
def mongo_db():
    from WeddingWebsite.extensions import mongo

    g_dict = {
        "_id": 0,
        "username": "username",
        "_password": "password",
        "name": "name",
        "email": "email@email.com",
        "roles": ["roles"],
        "party": ["Parties"],
    }
    Guest(**g_dict).add_to_mongodb(mongo.db)

    yield mongo.db

    mongo.db.drop_collection("guests")


def log_in(app, username="username", password="password"):
    response = app.post(
        "/auth/login",
        data={"username": username, "password": password},
        follow_redirects=True,
    )
    if b"Logged in" in response.data:
        return True
    return False
