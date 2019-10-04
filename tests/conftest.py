import hashlib
from unittest import mock

import pytest

from WeddingWebsite import create_app
from WeddingWebsite.auth import requires_roles, roles_cannot_access
from WeddingWebsite.config import TestingConfig
from WeddingWebsite.models import Guest


@pytest.fixture
def template_user():
    g_dict = {
        "_id": 0,
        "username": "t_template_user",
        "_password": "123456",
        "name": "t_template_user",
        "email": "t_template_user@test.org",
    }
    return Guest(**g_dict)


@pytest.fixture(scope="session")
def test_client():
    flask_app = create_app(TestingConfig)

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


@pytest.fixture(autouse=True)
def mongo_db(request, test_client):
    if "no_mongo_db" in request.keywords:
        yield None
    else:
        from WeddingWebsite.extensions import mongo

        # Add Guests
        # Add Default boring Guest
        Guest(
            _id=None,
            username="t_default",
            _password="123456",
            name="t_default",
            email="td@test.org",
        ).add_to_collection(mongo.db.guests)

        # Add Groomsman Tester
        Guest(
            _id=None,
            username="t_groomsman",
            _password="123456",
            name="t_groomsman",
            email="tg@test.org",
            roles=["groomsman"],
        ).add_to_collection(mongo.db.guests)

        # Add Bridesmaid Tester
        Guest(
            _id=None,
            username="t_bridesmaid",
            _password="123456",
            name="t_bridesmaid",
            email="tb@test.org",
            roles=["bridesmaid"],
        ).add_to_collection(mongo.db.guests)

        # Add Wedding Party Tester
        Guest(
            _id=None,
            username="t_wedding_party",
            _password="123456",
            name="t_wedding_party",
            email="twp@test.org",
            roles=["wedding_party"],
        ).add_to_collection(mongo.db.guests)

        # Add Admin Tester
        Guest(
            _id=None,
            username="t_admin",
            _password="123456",
            name="t_admin",
            email="ta@test.org",
            roles=["admin"],
        ).add_to_collection(mongo.db.guests)

        yield mongo.db

        mongo.db.guests.drop()


def log_in(app, username="t_default", password="123456"):
    response = app.post(
        "/auth/login",
        data={"username": username, "password": password},
        follow_redirects=True,
    )
    if b"Logged in" in response.data:
        return True
    return False


@pytest.fixture(autouse=True)
def mock_hashlib_pbkdf2(request):
    """
    Mocks the built in method hashlib.pbkdf2 to decrease test runtime.
    """
    if "no_mock_hashlib_pbkdf2" in request.keywords:
        yield None
    else:
        with mock.patch.object(
            hashlib, "pbkdf2_hmac", return_value=b"123465"
        ) as _mocked_hash:
            yield _mocked_hash
