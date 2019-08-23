from flask import Blueprint, render_template
from flask_login import fresh_login_required, login_required

from flaskr.auth import requires_roles


views = Blueprint("views", __name__, url_prefix="")


@views.route("/")
def index():
    return render_template("index.html")


@views.route("/member")
def member_page():
    return "This is the members only page"


@views.route("/view_profile")
@login_required
def view_profile():
    """
    Route for viewing profile info
    """
    return "This is the profile view"


@views.route("/edit_profile")
@fresh_login_required
def edit_profile():
    """
    Route for editing profile info
    """
    return "This is the edit profile view"


@views.route("/test_required_roles")
@requires_roles("test_role")
def test_required_roles():
    return "Congrats, you have the required roles"
