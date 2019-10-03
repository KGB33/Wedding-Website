import mongomock
import pytest

from WeddingWebsite.models import GuestCollection


@pytest.mark.no_mongo_db
def test_init_empty_db():
    """
    GIVEN an empty DB
    WHEN a Guest Collection is initialized
    THEN check that GuestCollection.guests is None
    """
    collection = mongomock.MongoClient().db.collection
    gc = GuestCollection(collection)
    assert not gc.guests


def test_init(mongo_db):
    """
    GIVEN a populated DB
    WHEN a Guest Collection is initialized
    THEN check that GuestCollection.guests contains all guests
    """
    gc = GuestCollection(mongo_db.guests)
    assert len(gc) == 5


def test_is_iterable(mongo_db):
    """
    GIVEN a (populated) Guest Collection
    WHEN it is iterated across
    THEN check that no errors are raised
    """
    gc = GuestCollection(mongo_db.guests)
    try:
        for _ in gc:
            continue
        assert True
    except TypeError:
        assert False


def test_str(mongo_db):
    """
    GIVEN a populated Guest Collection
    CHECK that the __str__ method acts as intended
    """
    gc = GuestCollection(mongo_db.guests)
    assert "Guests in collection:\n\tUser t_default, with id: " in str(gc)
