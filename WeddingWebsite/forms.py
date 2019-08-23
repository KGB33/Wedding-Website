from flask_wtf import FlaskForm
from wtforms import BooleanField, PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError

from WeddingWebsite import mongo


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
