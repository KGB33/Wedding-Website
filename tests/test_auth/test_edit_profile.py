from tests.conftest import log_in


class TestLoggedInUser:
    def test_view_page(self, test_client):
        log_in(test_client)
        response = test_client.get("/auth/edit_profile")
        assert response.status_code == 200
        assert b"<!-- guest_edit.html -->" in response.data

    def test_submit_page_no_change(self, test_client):
        log_in(test_client)
        response = test_client.post(
            "/auth/edit_profile", data={}, follow_redirects=True
        )
        assert (
            b"""<!-- guest.html -->
<head>
    <meta charset="UTF-8">
    <title> t_default </title>
</head>
<body>
    <h1>User t_default, with id: """
            in response.data
        )

        assert (
            b"""
    <ul>
        <li>Name: t_default</li>
        <li>Email: td@test.org</li>
        <li>Roles:
            
                None
            
        </li>
        <li>Party:
            
                None
            
        </li>
    </ul>

    <a href="/auth/edit_profile">Edit</a>

</body>"""
            in response.data
        )

    def test_submit_page_change_all(self, test_client, mongo_db):
        log_in(test_client)
        user_id = mongo_db.guests.find_one({"name": "t_default"})["_id"]
        response = test_client.post(
            "/auth/edit_profile",
            data={
                "username": "new_username",
                "name": "new_name",
                "email": "new_email@email.org",
            },
        )
        assert response.status_code == 302  # Redirected
        user = mongo_db.guests.find_one({"_id": user_id})
        assert user["name"] == "new_name"
        assert user["username"] == "new_username"
        assert user["email"] == "new_email@email.org"
