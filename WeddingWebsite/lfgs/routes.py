from flask_login import login_required, current_user
from flask import render_template, url_for, redirect
from flask_pymongo import ObjectId

from WeddingWebsite.lfgs import bp
from WeddingWebsite.lfgs.models import LFG, LFGCollection
from WeddingWebsite.lfgs.forms import (
    CreateLFGForm,
    EditLFGForm,
    ContactInfoForm,
    ConfirmActionForm,
)
from WeddingWebsite.extensions import mongo


@bp.route("/")
@login_required
def index():
    lfgs = LFGCollection(mongo.db.lfgs)
    return render_template(
        "lfgs.html",
        lfgs=lfgs.lfgs,
        is_in_lfg=(lambda g, cu: str(cu.id) in g.members.keys()),
    )


@bp.route("/<string:lfg_id>/join", methods=["GET", "POST"])
@login_required
def join_lfg(lfg_id):
    form = ContactInfoForm()
    lfg = LFG(**mongo.db.lfgs.find_one({"_id": ObjectId(lfg_id)}))
    if form.validate_on_submit():
        lfg.add_member(
            str(current_user.id),
            f"Name: {current_user.name}, Contact Info: {form.contact_info.data}",
        )
        lfg.update_collection(mongo.db.lfgs)
        return redirect(url_for("lfgs.index"))
    return render_template("join_lfg.html", form=form)


@bp.route("/<string:lfg_id>/edit", methods=["GET", "POST"])
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
        return redirect(url_for("lfgs.index"))
    return render_template("edit_lfg.html", lfg=lfg, form=form)


@bp.route("/<string:lfg_id>/leave")
@login_required
def leave_lfg(lfg_id):
    lfg = LFG(**mongo.db.lfgs.find_one({"_id": ObjectId(lfg_id)}))
    lfg.remove_member(str(current_user.id))
    lfg.update_collection(mongo.db.lfgs)
    return redirect(url_for("lfgs.index"))


@bp.route("/create", methods=["GET", "POST"])
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
        return redirect(url_for("lfgs.index"))
    return render_template("create_lfg.html", form=form)


@bp.route("/<string:lfg_id>/delete", methods=["GET", "POST"])
@login_required
def delete_lfg(lfg_id):
    lfg = LFG(**mongo.db.lfgs.find_one({"_id": ObjectId(lfg_id)}))
    if current_user.id != lfg.owner_id:
        return f"Cannot delete lfg you do not own. \n\n {lfg=}"
    form = ConfirmActionForm()
    if form.validate_on_submit():
        mongo.db.lfgs.delete_one({"_id": ObjectId(lfg_id)})
        return redirect(url_for("lfgs.index"))
    return render_template("confirm_action.html", form=form, action=f"Delete LFG")
