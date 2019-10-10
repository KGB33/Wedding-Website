from tests.conftest import log_in


def test_rsvp_first_visit(test_client):
    """
    GIVEN a flask app
    WHEN a user first visits '/rsvp'
    THEN check that the 'Current Status:' data displays
    """
    log_in(test_client)
    response = test_client.get("/rsvp")
    assert b"Current Status: []" in response.data


def test_rsvp_first_entry(test_client):
    """
    GIVEN a flask app
    When a user submits '/rsvp' for the first time
    THEN check that the data updates in the DB and on the page.
    """
    log_in(test_client)
    response = test_client.post(
        "/rsvp",
        data={
            "diet": ["no pork", "no gluten", "no nuts"],
            "status": "yes",
            "plus_one_status": "undecided",
        },
    )
    assert response.status_code == 200
    assert b"Current Status: yes" in response.data
    assert b"Current Status: undecided" in response.data


def test_rsvp_submit_form_empty_status(test_client):
    """
    GIVEN a flask app
    WHEN the user submits '/rsvp' where the form.status and form.plus_one_status is not provided
    THEN check that the value in the db is unchanged
    """
    log_in(test_client)
    response = test_client.post(
        "/rsvp", data={"diet": ["no pork", "no gluten", "no nuts"]}
    )
    assert response.status_code == 200
    assert response.data.count(b"[This field is required.]") == 2
