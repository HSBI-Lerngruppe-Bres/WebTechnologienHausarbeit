from flask import Blueprint, render_template, redirect, url_for, request, flash
from bruno.database.interaction.accounts import create_user
from flask_login import logout_user, login_user
from bruno.forms.accounts import CreateUserForm

site = Blueprint("accounts", __name__,
                 template_folder="templates/accounts", url_prefix="/accounts")


@site.route('/login_register', methods=['GET', 'POST'])
def login_register():
    """The login and register handler for post and get request. Using
       WTForms to validate the users input. login or register the user

    Returns:
        HTTPResponse: Either the side the user wants to be redirected to or the login and register form
    """
    # TODO redirect after logged in
    login_form = CreateUserForm(prefix='login')
    user = None
    if request.form and login_form.validate_on_submit():
        user = create_user(login_form.username.data)

    if user:
        login_user(user)

        next = request.args.get('next')
        # TODO possible security risk
        return redirect(next or url_for('sites.index'))
    return render_template('create_user.html', login_form=login_form)


@site.get("/logout")
def logout():
    """Listens to /logout via get and logs the user out.

    Returns:
        HTTPResponse: The redirect to the index page
    """
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for('sites.index'))
