from WeddingWebsite.mail import build_rsvp_email, get_recipients, Message, Recipient
from WeddingWebsite.models import GuestCollection


class TestSendMail:
    """
    Currently Unable to mock API call, not testing ATM
    """

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
    """
    Same as the Messages Constructor
    """

    pass


class TestGetRecipients:
    def test_send_to_all(self, mongo_db):
        recipients = get_recipients(send_to_all=True)
        expected = [
            Recipient(guest.email, guest.name)
            for guest in GuestCollection(mongo_db.guests)
        ]
        assert set(recipients) == set(expected)

    def test_require_all_roles(self, mongo_db, template_user):
        roles = ["cabin_stayer", "a made up role", "TesterJester"]
        template_user.roles = roles
        template_user.add_to_collection(mongo_db.guests)
        recipients = get_recipients(require_any_all_roles="all", recipient_roles=roles)
        expected = [Recipient(template_user.email, template_user.name)]
        assert expected == recipients

    def test_require_any_roles(self, template_user, mongo_db):
        roles = ["cabin_stayer", "a made up role", "TesterJester", "groomsman"]
        template_user.roles = roles
        template_user.add_to_collection(mongo_db.guests)

        recipients = get_recipients(require_any_all_roles="any", recipient_roles=roles)
        expected = [
            Recipient(template_user.email, template_user.name),
            Recipient("tg@test.org", "t_groomsman"),
        ]

        # Use sets to test regardless of order
        assert set(expected) == set(recipients)
