from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, RadioField, SubmitField
from wtforms.validators import InputRequired


class CreateLFGForm(FlaskForm):
    max_members = IntegerField(
        "Max Members (including yourself)", validators=[InputRequired()]
    )
    info = StringField(
        "Information that group members will need to know.",
        validators=[InputRequired()],
    )
    group_type = RadioField(
        "LFG Type",
        choices=[("CARPOOL", "Carpool"), ("HOTEL", "hotel")],
        validators=[InputRequired()],
    )

    submit = SubmitField("Create LFG!")


class EditLFGForm(FlaskForm):
    max_members = IntegerField("Max Members (including yourself)")
    info = StringField("Information that group members will need to know.",)
    group_type = RadioField(
        "LFG Type", choices=[("CARPOOL", "Carpool"), ("HOTEL", "hotel")],
    )

    submit = SubmitField("Make Changes!")


class ContactInfoForm(FlaskForm):
    contact_info = StringField(
        "Please enter your contact information.", validators=[InputRequired()]
    )
    submit = SubmitField("Join LFG!")


class ConfirmActionForm(FlaskForm):
    submit = SubmitField("Confirm Action!")
