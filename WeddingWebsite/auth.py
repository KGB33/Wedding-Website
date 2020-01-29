from functools import wraps

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_user, logout_user
from werkzeug.urls import url_parse

from WeddingWebsite import login_manager
from WeddingWebsite.exceptions import NoRolesProvided
from WeddingWebsite.extensions import mongo
from WeddingWebsite.forms import LoginForm, RegistrationForm
from WeddingWebsite.models import Guest


auth = Blueprint(
    "auth",
    __name__,
    url_prefix="/auth",
    template_folder="templates",
    static_folder="static",
)


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


@auth.route("/unauthorized_role")
def unauthorized_role():
    return "You are seeing this page because you lack the required roles to view your requested page."


def requires_roles(*roles):
    """
    Implements role biased authentication over Flask-login

    :param roles: Required Roles for authentication
    """

    def wrapper(func):
        @wraps(func)
        def decorated_view(*args, **kwargs):

            if not roles:
                raise NoRolesProvided(
                    "No Roles provided, Please use @login_required instead"
                )

            if not current_user.is_authenticated:
                return login_manager.unauthorized()

            if current_user.roles is None:
                return redirect(url_for("auth.unauthorized_role"))

            for role in roles:
                if role not in current_user.roles:
                    return redirect(url_for("auth.unauthorized_role"))
            return func(*args, **kwargs)

        return decorated_view

    return wrapper


def roles_cannot_access(*roles):
    """
    Implements role biased authentication over Flask-login

    Users with the provided roles CANNOT access the route.

    :param roles: Required Roles for authentication
    """

    def wrapper(func):
        @wraps(func)
        def decorated_view(*args, **kwargs):

            if not roles:
                raise NoRolesProvided(
                    "No Roles provided, Please use @login_required instead"
                )

            if not current_user.is_authenticated:
                return login_manager.unauthorized()

            if current_user.roles is None:
                return func(*args, **kwargs)

            for role in roles:
                if role in current_user.roles:
                    return redirect(url_for("auth.unauthorized_role"))
            return func(*args, **kwargs)

        return decorated_view

    return wrapper
