from tests.conftest import log_in


class TestDressCode:
    def test_dress_code_anon_user(self, test_client):
        """
        GIVEN a flask app
        WHEN an anon user requests '/dress_code'
        THEN Check that it redirects them to the login page
        """
        response = test_client.get("/dress_code", follow_redirects=True)
        assert response.status_code == 200
        assert b"Sign In" in response.data

    def test_dress_code_auth_user_no_roles(self, test_client):
        """
        GIVEN a flask app
        WHEN a auth user with no roles requests '/dress_code'
        THEN check that they are shown '/dress_code/default.html'
        """
        assert log_in(test_client)
        response = test_client.get("/dress_code")
        assert response.status_code == 200
        assert b"/dress_code/default.html" in response.data

    def test_dress_code_auth_user_bridesmaid_role(self, test_client):
        """
        GIVEN a flask app
        WHEN a auth user width the bridesmaid role requests '/dress_code'
        THEN check that they are redirected to '/dress_code/bridesmaid'
        """
        assert log_in(test_client, username="t_bridesmaid")
        response = test_client.get("/dress_code")
        assert response.status_code == 200
        assert b"/dress_code/bridesmaid.html" in response.data

    def test_dress_code_auth_user_groomsman_role(self, test_client):
        """
        GIVEN a flask app
        WHEN a auth user width the groomsman role requests '/dress_code'
        THEN check that they are redirected to '/dress_code/groomsmen'
        """
        assert log_in(test_client, username="t_groomsman")
        response = test_client.get("/dress_code")
        assert response.status_code == 200
        assert b"/dress_code/groomsmen.html" in response.data

    def test_dress_code_auth_user_bridesmaid_and_wedding_party_roles(
        self, test_client, template_user, mongo_db
    ):
        """
        GIVEN a flask app
        WHEN a auth user width the bridesmaid and wedding party roles requests '/dress_code'
        THEN check that they are redirected to '/dress_code/bridesmaid'
        """
        template_user.roles = ["bridesmaid", "wedding_party"]
        template_user.add_to_mongodb(mongo_db)
        assert log_in(test_client, username="t_template_user")
        response = test_client.get("/dress_code")
        assert response.status_code == 200
        assert b"/dress_code/bridesmaid.html" in response.data

    def test_dress_code_auth_user_groomsman_and_wedding_party_roles(
        self, test_client, template_user, mongo_db
    ):
        """
        GIVEN a flask app
        WHEN a auth user width the groomsman and wedding_party roles requests '/dress_code'
        THEN check that they are redirected to '/dress_code/groomsmen'
        """
        template_user.roles = ["groomsman", "wedding_party"]
        template_user.add_to_mongodb(mongo_db)
        assert log_in(test_client, username="t_template_user")
        response = test_client.get("/dress_code")
        assert response.status_code == 200
        assert b"/dress_code/groomsmen.html" in response.data

    def test_dress_code_auth_user_wedding_party_role(self, test_client):
        """
        GIVEN a flask app
        WHEN a auth user width the wedding_party role requests '/dress_code'
        THEN check that they are redirected to '/dress_code/wedding_party'
        """
        assert log_in(test_client, username="t_wedding_party")
        response = test_client.get("/dress_code")
        assert response.status_code == 200
        assert b"/dress_code/wedding_party.html" in response.data
