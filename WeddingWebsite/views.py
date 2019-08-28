from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import current_user, fresh_login_required, login_required

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
