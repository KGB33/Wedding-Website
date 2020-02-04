from flask import Blueprint

admin = Blueprint(
    "admin",
    __name__,
    url_prefix="/admin",
    template_folder="templates",
    static_folder="static",
)

from WeddingWebsite.admin import routes
