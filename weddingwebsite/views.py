from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import current_user, fresh_login_required, login_required
from flask_pymongo import ObjectId


from .extensions import mongo
from .forms import RSVPForm
from .models import GuestCollection


views = Blueprint("views", __name__, url_prefix="")


@views.route("/")
def index():
    # moved login page back due to COVID/Postponement
    """
    if current_user.is_authenticated:
        return redirect(url_for("views.home"))
    return render_template("index.html")
    """
    return redirect(url_for("views.home"))


@views.route("/home")
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
    if "cabin_stayer" in current_user.roles:
        return render_template("location_cabin.html")
    return render_template("location_hotel.html")


@views.route("/photos")
@login_required
def photos():
    return render_template("photos.html")


@views.route("/details")
@login_required
def details():
    return render_template("details.html", guest=current_user)
