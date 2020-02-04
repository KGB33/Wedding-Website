from flask_wtf import FlaskForm
from wtforms import (
    BooleanField,
    PasswordField,
    RadioField,
    SelectMultipleField,
    StringField,
    SubmitField,
    widgets,
    IntegerField,
)
from wtforms.validators import (
    DataRequired,
    Email,
    EqualTo,
    InputRequired,
    ValidationError,
)

from WeddingWebsite import mongo


class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class RSVPForm(FlaskForm):
    status_choices = ["yes", "no", "undecided"]
    diet_choices = [
        "no pork",
        "no beef",
        "no fowl",
        "no fish",
        "no meat",
        "no dairy",
        "no eggs",
        "no nuts",
        "no gluten",
    ]
    status = RadioField(
        "Going?",
        choices=[(x, x.title()) for x in status_choices],
        validators=[InputRequired()],
    )
    plus_one_status = RadioField(
        "Going?",
        choices=[(x, x.title()) for x in status_choices],
        validators=[InputRequired()],
    )
    diet = MultiCheckboxField(
        "Food Restrictions/allergies:", choices=[(x, x.title()) for x in diet_choices]
    )
    submit = SubmitField("Update RSVP")


class SendMailForm(FlaskForm):
    subject = StringField("Subject", validators=[InputRequired()])
    message = StringField("Message", validators=[InputRequired()])
    send_to_all = BooleanField("Send To All Guests")
    poss_roles = ["admin", "bridesmaid", "groomsmen", "wedding party", "cabin_stayers"]
    recipients = MultiCheckboxField(
        "Select roles:", choices=[(x, x.title()) for x in poss_roles]
    )
    require_any_all_roles = RadioField(
        choices=[("all", "all"), ("any", "any")], validators=[InputRequired()]
    )
    submit = SubmitField("Send Email")


class ConfirmActionForm(FlaskForm):
    submit = SubmitField("Confirm Action!")
