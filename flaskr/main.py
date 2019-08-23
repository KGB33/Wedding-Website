from flask import Blueprint, render_template


bp = Blueprint("main", __name__, url_prefix="")


@bp.route("/")
def index():
    return render_template("index.html")


@bp.route("/member")
def member_page():
    return "This is the members only page"
