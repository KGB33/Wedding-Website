from tests.conftest import log_in


def test_register_new_user(test_client, mongo_db):
    """
    GIVEN a Flask app
    WHEN a new guest registers
    THEN Check that the guest was added to the DB and is redirected
    """
    response = test_client.post(
        "/auth/register",
        data={
            "username": "username",
            "password": "password",
            "password2": "password",
            "name": "name",
            "email": "email@email.com",
        },
        follow_redirects=True,
    )
    # Check that the user was redirected
    assert response.status_code == 200
    assert b"Sign In" in response.data
    assert b"Congratulations, you are now a registered user!" in response.data

    # Check that the user was added to the db
    assert mongo_db.guests.find_one({"username": "username"})


def test_register_current_user_is_authenticated(test_client, mongo_db, new_guest):
    """
    GIVEN a flask app
    WHEN a authenticated user attempts to register
    THEN check that they are redirected to the index page
    """
    new_guest.add_to_mongodb(mongo_db)
    log_in("username", "password", test_client)
    response = test_client.post("/auth/register", follow_redirects=True)
    assert response.status_code == 200
    assert b"Hi username!" in response.data
    assert b"You are already logged in! No need to register." in response.data


def test_register_new_user_with_bad_info(test_client, mongo_db, new_guest):
    """
    GIVEN a Flask app
    WHEN a user attempts to create an account with a taken email/username
    THEN check that an error message is flashed, and that the new user was not added to the db
    """
    new_guest.add_to_mongodb(mongo_db)
    response = test_client.post(
        "/auth/register",
        data={  # Username and email taken by fixture 'new_user'
            "username": "username",
            "password": "password",
            "password2": "password",
            "name": "name",
            "email": "email@email.com",
        },
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert b"Please use a different username." in response.data
    assert b"Please use a different email address." in response.data
    assert b"Register" in response.data
