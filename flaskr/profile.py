from flask import Blueprint
from flask_login import fresh_login_required, login_required


bp = Blueprint("profile", __name__, url_prefix="/profile")


@bp.route("/view")
@login_required
def view():
    """
    Route for viewing profile info
    """
    return "This is the profile view"


@bp.route("/edit")
@fresh_login_required
def edit():
    """
    Route for editing profile info
    """
    return "This is the edit profile view"
