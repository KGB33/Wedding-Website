from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import current_user, fresh_login_required, login_required
from flask_pymongo import ObjectId


from WeddingWebsite.extensions import mongo
from WeddingWebsite.forms import (
    EditForm,
    RSVPForm,
    CreateLFGForm,
    EditLFGForm,
    ContactInfoForm,
    ConfirmActionForm,
)
from WeddingWebsite.models import GuestCollection, LFGCollection, LFG


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


@views.route("/view_profile")
@login_required
def view_profile():
    """
    Route for viewing profile info
    """
    return render_template("guest.html", guest=current_user)


@views.route("/edit_profile", methods=["GET", "POST"])
@fresh_login_required
def edit_profile():
    form = EditForm()
    guest = current_user
    if form.validate_on_submit():
        if form.username.data:
            guest.username = form.username.data
        if form.password.data:
            guest.password = form.password.data
        if form.name.data:
            guest.name = form.name.data
        if form.email.data:
            guest.email = form.email.data
        guest.update_collection(mongo.db.guests)
        return redirect(url_for("views.view_profile"))
    return render_template("guest_edit.html", guest=current_user, form=form)


@views.route("/lfgs")
@login_required
def lfgs():
    lfgs = LFGCollection(mongo.db.lfgs)
    return render_template("lfgs.html", lfgs=lfgs.lfgs, is_in_lfg=(lambda g, cu: str(cu.id) in g.members.keys()))


@views.route("/lfgs/<string:lfg_id>/join", methods=["GET", "POST"])
@login_required
def join_lfg(lfg_id):
    form = ContactInfoForm()
    lfg = LFG(**mongo.db.lfgs.find_one({"_id": ObjectId(lfg_id)}))
    if form.validate_on_submit():
        lfg.add_member(
                str(current_user.id), f"Name: {current_user.name}, Contact Info: {form.contact_info.data}"
        )
        lfg.update_collection(mongo.db.lfgs)
        return redirect(url_for("views.lfgs"))
    return render_template("join_lfg.html", form=form)


@views.route("/lfgs/<string:lfg_id>/edit", methods=["GET", "POST"])
@login_required
def edit_lfg(lfg_id):
    form = EditLFGForm()
    lfg = LFG(**mongo.db.lfgs.find_one({"_id": ObjectId(lfg_id)}))
    if form.validate_on_submit():
        if form.info.data:
            lfg.info = form.info.data
        if form.max_members.data:
            if lfg.total_members > form.max_members.data:
                flash("Cannot have total members be greater that the max members")
            else:
                lfg.max_members = int(form.max_members.data)
        if form.group_type.data:
            lfg.group_type = form.group_type.data
        lfg.update_collection(mongo.db.lfgs)
        return redirect(url_for("views.lfgs"))
    return render_template("edit_lfg.html", lfg=lfg, form=form)


@views.route("/lfgs/<string:lfg_id>/leave")
@login_required
def leave_lfg(lfg_id):
    lfg = LFG(**mongo.db.lfgs.find_one({"_id": ObjectId(lfg_id)}))
    lfg.remove_member(str(current_user.id))
    lfg.update_collection(mongo.db.lfgs)
    return redirect(url_for("views.lfgs"))


@views.route("/lfgs/create", methods=["GET", "POST"])
@login_required
def create_lfg():
    form = CreateLFGForm()
    if form.validate_on_submit():
        lfg = LFG(
            owner_id=current_user.id,
            owner_name=current_user.name,
            members=dict(),
            max_members=form.max_members.data,
            info=form.info.data,
            group_type=form.group_type.data,
        )
        lfg.add_to_collection(mongo.db.lfgs)
        return redirect(url_for("views.lfgs"))
    return render_template("create_lfg.html", form=form)

@views.route("/lfgs/<string:lfg_id>/delete", methods=["GET", "POST"])
@login_required
def delete_lfg(lfg_id):
    lfg = LFG(**mongo.db.lfgs.find_one({"_id": ObjectId(lfg_id)}))
    if current_user.id != lfg.owner_id:
        return f"Cannot delete lfg you do not own. \n\n {lfg=}"
    form = ConfirmActionForm()
    if form.validate_on_submit():
        mongo.db.lfgs.delete_one({"_id": ObjectId(lfg_id)})
        return redirect(url_for("views.lfgs"))
    return render_template('confirm_action.html', form=form, action=f"Delete LFG")

