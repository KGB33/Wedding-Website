from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import current_user, fresh_login_required, login_required

from WeddingWebsite.extensions import mongo
from WeddingWebsite.forms import EditForm, RSVPForm
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


@views.route("/rsvp", methods=["GET", "POST"])
@login_required
def rsvp():
    form = RSVPForm()
    if form.validate_on_submit():
        current_user.dietary_restrictions = form.diet.data
        current_user.RSVP_status = form.status.data
        current_user.plus_one = form.plus_one_status.data
        current_user.update_collection(mongo.db.guests)
    return render_template("RSVP.html", form=form, guest=current_user)


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
    return render_template("dress_code/default.html")


@views.route("/registry")
@login_required
def registry():
    return render_template("registry.html")


@views.route("/location")
@login_required
def location():
    if current_user.roles is not None:
        if "cabin_stayer" in current_user.roles:
            return render_template("location_cabin.html")
    return render_template("location_hotel.html")


@views.route("/photos")
@login_required
def photos():
    return render_template("photos.html")


@views.route("/view_profile")
@login_required
def view_profile():
    """
    Route for viewing profile info
    """
    return render_template("templates/guest.html", guest=current_user)


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
        guest.update_collection(mongo.db)
        flash("Changes Saved")
