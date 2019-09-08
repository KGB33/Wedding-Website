from flask import Blueprint, flash, redirect, render_template, url_for

from WeddingWebsite.auth.auth import requires_roles
from WeddingWebsite.extensions import mongo
from WeddingWebsite.forms import EditForm
from WeddingWebsite.models import GuestCollection


admin = Blueprint(
    "admin",
    __name__,
    url_prefix="/admin",
    template_folder="templates",
    static_folder="static",
)


@admin.route("/")
@admin.route("/guests")
@requires_roles("admin")
def index():
    guests = GuestCollection()
    return render_template("dashboard_guests.html", guests=guests)


@admin.route("/guest/<guest_id>")
@requires_roles("admin")
def view_guest(guest_id):
    guest = GuestCollection().get_guest_by_id(guest_id)
    return render_template("guest.html", guest=guest)


@admin.route("/guest/<guest_id>/edit", methods=["GET", "POST"])
@requires_roles("admin")
def edit_guest(guest_id):
    guest = GuestCollection().get_guest_by_id(guest_id)
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
        return redirect(url_for("admin.view_guest", guest_id=guest_id))
    return render_template("guest_edit.html", guest=guest, form=form)
