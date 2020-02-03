from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_user, logout_user, fresh_login_required
from werkzeug.urls import url_parse

from WeddingWebsite import login_manager
from WeddingWebsite.auth.exceptions import NoRolesProvided
from WeddingWebsite.extensions import mongo
from WeddingWebsite.auth.forms import LoginForm, RegistrationForm
from WeddingWebsite.models import Guest
from WeddingWebsite.auth import auth


@auth.route("/refresh_login", methods=["GET", "POST"])
def refresh_login():
    if current_user:
        logout_user()

    form = LoginForm()
    if form.validate_on_submit():
        try:
            guest = Guest(**mongo.db.guests.find_one({"username": form.username.data}))
        except TypeError:
            guest = None
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


@auth.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        flash("You are already logged in!")
        return redirect(url_for("views.index"))
    form = LoginForm()
    if form.validate_on_submit():
        try:
            guest = Guest(**mongo.db.guests.find_one({"username": form.username.data}))
        except TypeError:
            guest = None
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


@auth.route("/logout")
def logout():
    if current_user.is_authenticated:
        logout_user()
        flash("You have been logged out.")
    else:
        flash("You were not, and still are not, logged in.")
    return redirect(url_for("views.index"))


@auth.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        flash("You are already logged in! No need to register.")
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
        guest.add_roles_from_code(form.code.data)
        guest.add_to_collection(mongo.db.guests)
        flash("Congratulations, you are now a registered user!")
        return redirect(url_for("auth.login"))
    return render_template("register.html", title="Register", form=form)


@auth.route("/edit_profile", methods=["GET", "POST"])
@fresh_login_required
def edit_profile():
    form = EditForm()
    guest = current_user
    if form.validate_on_submit():
        if form.username.data:
            guest.username = form.username.data
        if form.password.data:
            guest.password = form.password.data
        if form.name.data:
            guest.name = form.name.data
        if form.email.data:
            guest.email = form.email.data
        guest.update_collection(mongo.db.guests)
        return redirect(url_for("views.view_profile"))
    return render_template("guest_edit.html", guest=current_user, form=form)


@auth.route("/unauthorized_role")
def unauthorized_role():
    return "You are seeing this page because you lack the required roles to view your requested page."
