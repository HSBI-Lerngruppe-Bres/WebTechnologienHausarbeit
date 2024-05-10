from flask import Blueprint, render_template, redirect, url_for, request, flash
from bruno.database.interaction.accounts import authenticate_user, register_user
from flask_login import logout_user, login_user
from bruno.forms.accounts import LoginForm, RegisterForm


site = Blueprint("accounts", __name__,
                 template_folder="templates/accounts", url_prefix="/accounts")


@site.route('/login_register', methods=['GET', 'POST'])
def login_register():
    """The login and register handler for post and get request. Using
       WTForms to validate the users input. login or register the user

    Returns:
        HTTPResponse: Either the side the user wants to be redirected to or the login and register form
    """
    # TODO redirect if already logged in
    login_form = LoginForm(prefix='login')
    register_form = RegisterForm(prefix='register')
    user = None
    if 'login_submit' in request.form and login_form.validate_on_submit():
        user = authenticate_user(request.form.get("Username"),
                                 request.form.get("Password"))
    elif 'register_submit' in request.form and register_form.validate_on_submit():
        user = register_user(request.form.get("Username"), request.form.get(
            "Password"), request.form.get("Confirm Password"), request.form.get("Email"))

    if user:
        login_user(user)
        return redirect(url_for('sites.index'))
    return render_template('login_register.html', login_form=login_form, register_form=register_form)


@site.get("/logout")
def logout():
    """Listens to /logout via get and logs the user out.

    Returns:
        HTTPResponse: The redirect to the index page
    """
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for('sites.index'))
