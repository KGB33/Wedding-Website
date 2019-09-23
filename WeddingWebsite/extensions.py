from dataclasses import asdict, dataclass

from flask_login import LoginManager
from flask_pymongo import PyMongo

from WeddingWebsite.exceptions import NoContentProvided


# Create PyMongo DB
mongo = PyMongo()

# Create login manager
login_manager = LoginManager()


# Mail
class Message:
    def __init__(
        self,
        subject=None,
        text_part=None,
        html_part=None,
        from_name="HannahAndKelton",
        from_email="hannahandkelton@bassingthwaite.org",
        recipients=None,
    ):
        self.subject = subject
        if text_part is None and html_part is None:
            raise NoContentProvided("Cannot send Message with No Content")
        self.text_part = text_part
        self.html_part = html_part
        self.recipients = recipients
        self.from_name = from_name
        self.from_email = from_email

    def as_dict(self):
        data = {
            "Messages": [
                {
                    "From": {"Email": self.from_email, "Name": self.from_name},
                    "Subject": self.subject,
                    "TextPart": self.text_part,
                    "HtmlPart": self.html_part,
                    "To": [asdict(r) for r in self.recipients],
                }
            ]
        }
        return data


@dataclass()
class Recipient:
    Email: str
    Name: str
