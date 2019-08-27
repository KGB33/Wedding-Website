import pytest

from WeddingWebsite import create_app
from WeddingWebsite.models import Guest


@pytest.fixture
def new_guest():
    g_dict = {
        "_id": 0,
        "username": "username",
        "_password": "password",
        "name": "name",
        "email": "email",
        "roles": ["roles"],
        "party": ["Parties"],
    }
    return Guest(**g_dict)


@pytest.fixture
def test_client():
    flask_app = create_app(test_config="../tests/flask_test.py")
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
