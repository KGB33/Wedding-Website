from tests.conftest import log_in


def get_guest_id(db, username="t_default"):
    return db.guests.find_one({"username": username})["_id"]


def test_admin_guest_view_default_guest(test_client, mongo_db):
    """
    GIVEN a flask app
    WHEN '/auth/guests/<guest_id>' is requested with 't_default's ID
    THEN check that 't_default's data is displayed
    """
    log_in(test_client, username="t_admin")
    response = test_client.get(
        f"/admin/guest/{get_guest_id(mongo_db)}", follow_redirects=True
    )
    assert response.status_code == 200
    assert b"<title> t_default </title>" in response.data
    assert b"<li>Name: t_default</li>" in response.data
    assert b"<li>Email: td@test.org</li>" in response.data
    assert b"<li>Roles:\n            \n                None" in response.data
