from tests.conftest import log_in


class TestDashboardAccess:
    def test_anon_user(self, test_client):
        """
        GIVEN a flask app
        WHEN an anon user requests '/admin'
        THEN check that they are redirected to the sign in page
        """
        response = test_client.get("/admin", follow_redirects=True)
        assert response.status_code == 200
        assert b"Sign In" in response.data

    def test_auth_user_without_admin_role(self, test_client):
        """
        GIVEN a flask app
        WHEN an authorized user w/o the admin role requests '/admin'
        THEN check that they are redirected to '/auth/unauthorized_role'
        """
        assert log_in(test_client)
        response = test_client.get("/admin", follow_redirects=True)
        assert response.status_code == 200
        assert (
            b"you lack the required roles to view your requested page." in response.data
        )

    def test_auth_user_with_admin_role(self, test_client):
        """
        GIVEN a flask app
        WHEN an authorized user w/ the admin role requests '/admin'
        THEN check that the page is rendered
        """
        assert log_in(test_client, username="t_admin")
        response = test_client.get("/admin", follow_redirects=True)
        assert response.status_code == 200
        assert b"<h1>Guests:</h1>" in response.data
        assert b"User t_admin," in response.data


class TestDashboardView:
    def test_template_render(self, test_client):
        """
        GIVEN a flask app
        WHEN the '/admin' page is requested by the appropriate user
        THEN check that the template displays all registered users appropriately
        """
        assert log_in(test_client, username="t_admin")
        response = test_client.get("/admin", follow_redirects=True)
        assert response.status_code == 200
        assert b"<h1>Guests:</h1>" in response.data
        assert b"User t_admin," in response.data
        assert b"User t_groomsman" in response.data
        assert b"User t_bridesmaid" in response.data
        assert b"User t_wedding_party" in response.data
        assert b"User t_default" in response.data

    def test_admin_and_admin_guests(self, test_client):
        """
        GIVEN a flask app
        CHECK that the routes '/admin' and '/admin/guest' return the same content
        """
        assert log_in(test_client, username="t_admin")
        response_1 = test_client.get("/admin/")
        response_2 = test_client.get("/admin/guests", follow_redirects=True)
        assert response_1.status_code == 200
        assert response_2.status_code == 200
        assert response_1.data == response_2.data
