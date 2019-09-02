from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import current_user, fresh_login_required, login_required

from WeddingWebsite.auth import requires_roles, roles_cannot_access
from WeddingWebsite.extensions import mongo
from WeddingWebsite.forms import EditForm
from WeddingWebsite.models import GuestCollection


views = Blueprint("views", __name__, url_prefix="")


@views.route("/")
def index():
    if current_user.is_authenticated:
        return redirect(url_for("views.home"))
    return render_template("index.html")


@views.route("/home")
@login_required
def home():
    return render_template("home.html")


@views.route("/rsvp")
@login_required
def rsvp():
    return "RSVP Page"


@views.route("/dress_code")
@login_required
def dress_code():
    if current_user.roles is None:
        return render_template("dress_code/default.html")
    if "bridesmaid" in current_user.roles:
        return render_template("dress_code/bridesmaid.html")
    if "groomsman" in current_user.roles:
        return render_template("dress_code/groomsmen.html")
    if "wedding_party" in current_user.roles:
        return render_template("dress_code/wedding_party.html")


@views.route("/registry")
@login_required
def registry():
    return "This is the registry page"


@views.route("/location")
@login_required
def location():
    if "cabin_stayer" in current_user.roles:
        return redirect(url_for("views.location_cabin"))
    else:
        return redirect(url_for("views.location_hotel"))


@views.route("/location/cabin")
@requires_roles("cabin_stayer")
def location_cabin():
    return "You are staying in the cabin"


@views.route("/location/hotel")
@roles_cannot_access("cabin_stayer")
def location_hotel():
    return "You will be staying in a hotel."


@views.route("/photos")
@login_required
def photos():
    return "This will be the photo place"


@views.route("/view_profile")
@login_required
def view_profile():
    """
    Route for viewing profile info
    """
    return render_template("admin/guest.html", guest=current_user)


@views.route("/edit_profile")
@fresh_login_required
def edit_profile():
    # TODO: add tests
    guest = GuestCollection().get_guest_by_id(current_user.id)
    form = EditForm()
    if form.validate_on_submit():
        if form.username.data:
            guest.username = form.username.data
        if form.password.data:
            guest.password = form.password.data
        if form.name.data:
            guest.name = form.name.data
        if form.email.data:
            guest.email = form.email.data
        guest.update_db(mongo.db)
        flash("Changes Saved")
