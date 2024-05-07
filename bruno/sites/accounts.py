from flask import Blueprint, render_template
#from flask_login import

site = Blueprint("accounts", __name__, template_folder="templates/accounts", url_prefix="/accounts")

@site.get("/login")
def login():
    return render_template("login.html")

@site.post("/login")
def login_post():
    return "Hallo"

@site.get("/register")
def register():
    return render_template("login.html")

@site.post("/login")
def register_post():
    return "Hallo"

@site.get("/logout")
def logout():
    return render_template("logout.html")