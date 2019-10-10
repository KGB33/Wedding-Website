from flask import Blueprint, flash, redirect, render_template, url_for

from WeddingWebsite.auth import requires_roles
from WeddingWebsite.extensions import mongo
from WeddingWebsite.forms import ConfirmActionForm, EditForm, SendMailForm
from WeddingWebsite.mail import build_custom_email, build_rsvp_email, get_recipients
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
    guests = GuestCollection(mongo.db.guests)
    return render_template("dashboard_guests.html", guests=guests)


@admin.route("/guest/<guest_id>")
@requires_roles("admin")
def view_guest(guest_id):
    guest = GuestCollection(mongo.db.guests).get_guest_by_id(guest_id)
    return render_template("guest.html", guest=guest)


@admin.route("/guest/<guest_id>/edit", methods=["GET", "POST"])
@requires_roles("admin")
def edit_guest(guest_id):
    guest = GuestCollection(mongo.db.guests).get_guest_by_id(guest_id)
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
        return redirect(url_for("admin.view_guest", guest_id=guest_id))
    return render_template("guest_edit.html", guest=guest, form=form)


@admin.route("/send_rsvp_reminder", methods=["GET", "POST"])
@requires_roles("admin")
def send_rsvp_reminder():
    form = ConfirmActionForm()
    if form.validate_on_submit():
        msg = build_rsvp_email()
        response = send_email(msg)
        return response.json()
    return render_template("send_rsvp_reminder.html", form=form)


@admin.route("/send_email", methods=["GET", "POST"])
@requires_roles("admin")
def send_email():
    form = SendMailForm()
    if form.validate_on_submit():
        recipients = get_recipients(
            send_to_all=form.send_to_all.data,
            require_any_all_roles=form.require_any_all_roles.data,
            recipient_roles=form.recipients.data,
        )
        msg = build_custom_email(form.subject.data, form.message.data, recipients)
        response = send_email(msg)
        return response.json()
    return render_template("send_email.html", form=form)
