from flask import Blueprint,render_template
from .accounts import site as account_site

site = Blueprint("sites", __name__, template_folder="templates", url_prefix="/")
site.register_blueprint(account_site)

@site.get("/")
def index():
    return render_template("index.html")