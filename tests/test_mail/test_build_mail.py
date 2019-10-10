import pytest

from WeddingWebsite.mail import build_rsvp_email, Message, Recipient
from WeddingWebsite.models import GuestCollection


class TestSendMail:
    pass


class TestBuildRsvpEmail:
    def test_build_rsvp(self, mongo_db):
        recipients = [
            Recipient(guest.email, guest.name)
            for guest in GuestCollection(mongo_db.guests)
            if guest.RSVP_status is None or guest.RSVP_status == "undecided"
        ]
        expt_msg = Message(
            subject="Répondez s'il vous plaît!",
            text_part="Please Update Your RSVP Status!",
            recipients=recipients,
        )
        msg = build_rsvp_email()
        assert expt_msg == msg


class TestBuildCustomEmail:
    @pytest.fixture(params=[])
    def expected_custom(self):
        pass

    def test_build_send_to_all(self):
        pass
