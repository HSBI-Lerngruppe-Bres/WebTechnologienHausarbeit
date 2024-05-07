from flask import Blueprint
from .account import site as account_site

site = Blueprint("site", __name__, template_folder="templates", url_prefix="/")
site.register_blueprint(account_site)

@site.get("/")
def index():
