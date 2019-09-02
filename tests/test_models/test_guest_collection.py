from WeddingWebsite.models import GuestCollection


def test_init_empty_db(mongo_db):
    """
    GIVEN an empty DB
    WHEN a Guest Collection is initialized
    THEN check that GuestCollection.guests is None
    """
    mongo_db.drop_collection("guests")
    gc = GuestCollection()
    assert not gc.guests


def test_init(mongo_db):
    """
    GIVEN a populated DB
    WHEN a Guest Collection is initialized
    THEN check that GuestCollection.guests contains all guests
    """
    gc = GuestCollection()
    assert len(gc) == 4


def test_is_iterable(mongo_db):
    """
    GIVEN a (populated) Guest Collection
    WHEN it is iterated across
    THEN check that no errors are raised
    """
    gc = GuestCollection()
    try:
        for g in gc:
            continue
        assert True
    except TypeError:
        assert False


def test_str(mongo_db):
    """
    GIVEN a populated Guest Collection
    CHECK that the __str__ method acts as intended
    """
    gc = GuestCollection()
    assert "Guests in collection:\n\tUser t_default, with id: " in str(gc)
