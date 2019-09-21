from flask import Blueprint, flash, redirect, render_template, url_for
from mailjet_rest import Client as MJClient

from WeddingWebsite.auth import requires_roles
from WeddingWebsite.extensions import Message, mongo, Recipient
from WeddingWebsite.forms import ConfirmActionForm, EditForm, SendMailForm
from WeddingWebsite.models import GuestCollection
from WeddingWebsite.secrets import MJ_KEY, MJ_PASSWORD


admin = Blueprint(
    "admin",
    __name__,
    url_prefix="/admin",
    template_folder="templates",
    static_folder="static",
)

mail_jet = MJClient(auth=(MJ_KEY, MJ_PASSWORD), version="v3.1")


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


@admin.route("/send_rsvp_reminder", methods=["GET", "POST"])
@requires_roles("admin")
def send_rsvp_reminder():
    form = ConfirmActionForm()
    if form.validate_on_submit():
        recipients = [
            Recipient(guest.email, guest.name)
            for guest in GuestCollection()
            if guest.RSVP_status is None or guest.RSVP_status == "undecided"
        ]
        msg = Message(
            subject="Répondez s'il vous plaît!",
            text_part="Please Update Your RSVP Status!",
            recipients=recipients,
        )
        response = mail_jet.send.create(data=msg.as_dict())
        return response.json()
    return render_template("send_rsvp_reminder.html", form=form)


@admin.route("/send_email", methods=["GET", "POST"])
@requires_roles("admin")
def send_email():
    form = SendMailForm()
    if form.validate_on_submit():
        if form.send_to_all.data:
            recipients = [
                Recipient(guest.email, guest.name) for guest in GuestCollection()
            ]
        elif form.require_any_all_roles.data == "all":
            recipients = [
                Recipient(guest.email, guest.name)
                for guest in GuestCollection()
                if all(role in guest.roles for role in form.recipients.data)
            ]
        else:
            recipients = [
                Recipient(guest.email, guest.name)
                for guest in GuestCollection()
                if any(role in guest.roles for role in form.recipients.data)
            ]
        msg = Message(
            text_part=form.message.data,
            subject=form.subject.data,
            recipients=recipients,
        )
        response = mail_jet.send.create(data=msg.as_dict())
        return response.json()
    return render_template("send_email.html", form=form)
