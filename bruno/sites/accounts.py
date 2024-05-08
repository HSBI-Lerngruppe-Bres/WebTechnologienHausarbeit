from flask import Blueprint, render_template, redirect, url_for, request, flash
from bruno.utils.accounts import authenticate_user, register_user
from flask_login import logout_user


site = Blueprint("accounts", __name__, template_folder="templates/accounts", url_prefix="/accounts")

@site.get("/login")
def login():
    #TODO redirect if already logged in
    return render_template("login.html")

@site.post("/login")
def login_post():
    username = request.form["username"].strip()
    password = request.form["password"].strip()
    if not authenticate_user(username, password):       
        return render_template("login.html")
    return redirect(url_for('sites.index'))
    #TODO redirect to redirect URL

@site.get("/register")
def register():
    #TODO redirect if already logged in
    return render_template("login.html")

@site.post("/register")
def register_post():
    username = request.form["username"]
    password = request.form["password"]
    if not register_user(username, password):
        return render_template("login.html")
    return redirect(url_for('sites.index'))

@site.get("/logout")
def logout():
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for('sites.index'))