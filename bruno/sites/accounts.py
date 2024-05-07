from flask import Blueprint, render_template
site = Blueprint("accounts", __name__, template_folder="templates", url_prefix="/accounts")

@site.get("/login")
def login():
    return render_template("login.html")

@site.get("/logout")
def logout():
    return render_template("logout.html")