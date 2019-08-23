from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_user, logout_user
from werkzeug.urls import url_parse

from flaskr.extensions import mongo
from flaskr.forms import LoginForm, RegistrationForm
from flaskr.models import Guest


bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        guest = Guest(**mongo.db.guests.find_one({"username": form.username.data}))
        if guest is None or not guest.check_password(form.password.data):
            flash("Invalid username or password")
            return redirect(url_for("auth.login"))
        login_user(guest, remember=form.remember_me.data)

        flash(f"Logged in {guest.name} successfully")

        next_url = request.args.get("next")
        if not next_url or url_parse(next_url).netloc != "":
            next_url = url_for("views.index")
        return redirect(next_url)
    return render_template("login.html", form=form)


@bp.route("/logout")
def logout():
    if current_user is not None:
        logout_user()
        flash("You have been logged out.")
    else:
        flash("You are not logged in.")
    return redirect(url_for("views.index"))


@bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("views.index"))
    form = RegistrationForm()
    if form.validate_on_submit():
        guest = Guest(
            None,
            form.username.data,
            form.password.data,
            form.name.data,
            form.email.data,
        )
        guest.add_to_mongodb(mongo.db)
        flash("Congratulations, you are now a registered user!")
        return redirect(url_for("auth.login"))
    return render_template("register.html", title="Register", form=form)
