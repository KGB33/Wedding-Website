from dataclasses import asdict

import pytest

from WeddingWebsite.exceptions import NoContentProvided
from WeddingWebsite.extensions import Message, Recipient


class TestMessage:
    def test_default_values(self):
        """ Asserts that the default values work as expected. """
        msg = Message(text_part="")
        assert msg.subject is None
        assert msg.html_part is None
        assert msg.text_part == ""
        assert msg.from_name == "HannahAndKelton"
        assert msg.from_email == "hannahandkelton@bassingthwaite.org"
        assert msg.recipients is None

    def test_no_text_and_no_html(self):
        """
        WHEN a Message is instantiated without a body (no text or html)
        ASSERT that the NoContentProvided Error is raised
        """
        with pytest.raises(NoContentProvided) as excinfo:
            msg = Message()
        assert "Cannot send Message with No Content" in str(excinfo.value)

    def test_as_dict(self):
        """
        GIVEN a Message Object
        WHEN Message.as_dict() is called
        THEN Check that the result matches the same pattern that the MailJet API expects
        """
        msg = Message(text_part="Text_Part", recipients=[Recipient("Email", "Name")])
        expected = {
            "Messages": [
                {
                    "From": {
                        "Email": "hannahandkelton@bassingthwaite.org",
                        "Name": "HannahAndKelton",
                    },
                    "Subject": None,
                    "TextPart": "Text_Part",
                    "HtmlPart": None,
                    "To": {"Email": "Email", "Name": "Name"},
                }
            ]
        }
        assert expected.keys() == msg.as_dict().keys()


class TestRecipient:
    def test_init(self):
        """
        Test Instantiating Recipient Object
        """
        r = Recipient("test@email.com", "Sr.Tester")
        assert r.Email == "test@email.com"
        assert r.Name == "Sr.Tester"

    def test_as_dict(self):
        """
        GIVEN a Recipient Object, 'r'
        WHEN asdict(r) is called
        THEN Check that the result matches the same pattern that the MailJet API expects
        """
        r = Recipient("test@email.com", "Sr.Tester")
        expected = {"Email": "test@email.com", "Name": "Sr.Tester"}
        assert expected == asdict(r)
