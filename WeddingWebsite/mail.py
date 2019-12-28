from dataclasses import asdict, dataclass

from mailjet_rest import Client as MJClient

from WeddingWebsite.exceptions import NoContentProvided
from WeddingWebsite.extensions import mongo
from WeddingWebsite.models import GuestCollection
from WeddingWebsite.secrets import MJ_KEY, MJ_PASSWORD


mail_jet = MJClient(auth=(MJ_KEY, MJ_PASSWORD), version="v3.1")


def send_mail_jet(msg):
    return mail_jet.send.create(data=msg.as_dict())


def build_rsvp_email():
    recipients = [
        Recipient(guest.email, guest.name)
        for guest in GuestCollection(mongo.db.guests)
        if guest.RSVP_status is None or guest.RSVP_status == "undecided"
    ]
    msg = Message(
        subject="Répondez s'il vous plaît!",
        text_part="Please Update Your RSVP Status!",
        recipients=recipients,
    )
    return msg


def build_custom_email(subject, body, recipients):
    msg = Message(text_part=body, subject=subject, recipients=recipients)
    return msg


def get_recipients(
    send_to_all=False, recipient_roles=None, require_any_all_roles="all"
):
    if send_to_all:
        recipients = [
            Recipient(guest.email, guest.name)
            for guest in GuestCollection(mongo.db.guests)
        ]
    elif require_any_all_roles == "all":
        recipients = [
            Recipient(guest.email, guest.name)
            for guest in GuestCollection(mongo.db.guests)
            if all(role in guest.roles for role in recipient_roles)
        ]
    elif require_any_all_roles == "any":
        recipients = [
            Recipient(guest.email, guest.name)
            for guest in GuestCollection(mongo.db.guests)
            if any(role in guest.roles for role in recipient_roles)
        ]
    else:
        return None
    return recipients


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

    def __eq__(self, other):
        return all(
            [
                self.subject == other.subject,
                self.text_part == other.text_part,
                self.html_part == other.html_part,
                self.recipients == other.recipients,
                self.from_name == other.from_name,
                self.from_email == other.from_email,
            ]
        )


@dataclass(eq=True, frozen=True)
class Recipient:
    Email: str
    Name: str
