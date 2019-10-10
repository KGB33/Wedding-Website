from tests.conftest import log_in


class TestCabinLocation:
    def test_cabin_role(self, test_client, mongo_db, template_user):
        template_user.roles = ["cabin_stayer"]
        template_user.add_to_collection(mongo_db.guests)
        log_in(test_client, username="t_template_user")
        response = test_client.get("/location")
        assert response.status_code == 200
        assert b"<!-- location_cabin.html -->" in response.data


class TestHotelLocation:
    def test_no_cabin_role(self, test_client):
        log_in(test_client)
        response = test_client.get("/location")
        assert response.status_code == 200
        assert b"<!-- location_hotel.html -->" in response.data
