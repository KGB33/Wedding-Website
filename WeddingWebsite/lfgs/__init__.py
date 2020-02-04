from flask import Blueprint

bp = Blueprint(
    "lfgs",
    __name__,
    url_prefix="/lfgs",
    template_folder="templates",
    static_folder="static",
)

from WeddingWebsite.lfgs import routes
