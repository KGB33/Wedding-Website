from flask_wtf import FlaskForm
from wtforms import (
    BooleanField,
    PasswordField,
    RadioField,
    SelectMultipleField,
    StringField,
    SubmitField,
    widgets,
)
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError

from WeddingWebsite import mongo


class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class LoginForm(FlaskForm):
    username = StringField("Username")
    password = PasswordField("Password")
    submit = SubmitField("Submit")
    remember_me = BooleanField("Remember Me")


class RegistrationForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    password2 = PasswordField(
        "Repeat Password", validators=[DataRequired(), EqualTo("password")]
    )
    email = StringField("Email", validators=[DataRequired(), Email()])
    submit = SubmitField("Register")

    def validate_username(self, username):
        user = mongo.db.guests.find_one({"username": username.data})
        if user is not None:
            raise ValidationError("Please use a different username.")

    def validate_email(self, email):
        user = mongo.db.guests.find_one({"email": email.data})
        if user is not None:
            raise ValidationError("Please use a different email address.")


class EditForm(FlaskForm):
    name = StringField("Name")
    username = StringField("Username")
    password = PasswordField("Password")
    password2 = PasswordField("Repeat Password", validators=[EqualTo("password")])
    email = StringField("Email")
    submit = SubmitField("Update Info")

    def validate_username(self, username):
        user = mongo.db.guests.find_one({"username": username.data})
        if user is not None:
            raise ValidationError("Please use a different username.")

    def validate_email(self, email):
        user = mongo.db.guests.find_one({"email": email.data})
        if user is not None:
            raise ValidationError("Please use a different email address.")


class RSVPForm(FlaskForm):
    status_choices = ["yes", "no", "maybe"]
    diet_choices = [
        "no pork",
        "no beef",
        "no fowl",
        "no fish",
        "no meat",
        "no dairy",
        "no eggs",
        "no nuts",
    ]
    status = RadioField("Going?", choices=[(x, x.title()) for x in status_choices])
    diet = MultiCheckboxField(
        "Food Restrictions/allergies:", choices=[(x, x.title()) for x in diet_choices]
    )
    submit = SubmitField("Update RSVP")
