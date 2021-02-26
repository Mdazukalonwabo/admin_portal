import os
from flask import render_template, url_for, flash, redirect, request, Blueprint

from flaskblog.users.forms import RegistrationForm, LoginForm, UpdateAccountForm, ActiveAccountForm
from flaskblog.models import User, Student, StaffMember
from flaskblog import app, db, bcrypt
from flaskblog.users.utlis import save_picture
from flaskblog.users.user_type import permissions

from flask_login import login_user, current_user, logout_user, login_required

from sqlalchemy import exc


users = Blueprint("users", __name__)


@users.route('/register', methods=['GET', 'POST'])    # the route and the methods the route can accept
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    form = RegistrationForm()
    if form.validate_on_submit():
        try:
            # create a hashed version of the users password
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")

            # set the account active if the new user is a visitor the account will be activated
            if form.type.data == 'visitor':
                active = True
            else:
                active = False
            # create an instance of the new user into the database
            user = User(username=form.username.data, email=form.email.data, password=hashed_password,
                        ID_number=form.id_number.data, first_name=form.first_name.data, last_name=form.last_name.data,
                        phone_number=form.phone_number.data, active=active, user_type=form.type.data)

            db.session.add(user)
            db.session.commit()
            user_tables(form.type.data, user)
            # once the user has been successfully registered
            flash(f'Your account has been created!', 'success')
            # will be redirected to login page
            return redirect(url_for('users.registration_success'))
        except exc.IntegrityError as e:
            flash(e)
            return render_template('register.html', title="Register", form=form)
    return render_template('register.html', title="Register", form=form)


# this function is used to add the users that are not visitors to their respective table
def user_tables(user_type, user):
    if user_type == "student":
        student = Student(user_id=user.id)
        db.session.add(student)
    elif user_type == "staff" or "business_unit":
        staff = StaffMember(user_id=user.id)
        db.session.add(staff)
    return db.session.commit()


@users.route('/registration-success')
def registration_success():
    return render_template('registration_success.html')


@users.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            password_valid = bcrypt.check_password_hash(user.password, form.password.data)
            if password_valid:
                if not user.active:
                    # redirect users with inactive accounts
                    return redirect(url_for("users.registeration_success"))
                # login the user
                login_user(user, remember=form.remember.data)
                # once the user has been successfully registered
                flash(f'You have been logged in!', 'success')
                next_page = request.args.get('next')    # to check if there isn't a next in the url
                """
                the statement below can be simplified as follow
                return redirect(next_page) if next_page else return redirect(url_for('home'))
                """
                if next_page:

                    return redirect(next_page)
                # will be redirected to this page
                return redirect(url_for('automation.covid_questionnaire'))
            else:
                flash("Login Unsuccessful. Please check email or password", 'danger')
        else:
            flash("Login Unsuccessful. Please check email or password", 'danger')
    return render_template('login.html', title="login", form=form)


@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('users.login'))


@users.route('/account', methods=['GET', 'POST'])
@login_required  # to redirect in case the user is not authenticated
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            # find the current image in the folder and delete it
            current_user_image = os.path.join(app.root_path, 'static/media/profile_pics', current_user.image_file)
            os.remove(current_user_image)
            # add the new image and save it into the database and the profile_pic path
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        # Update the users details with the new data
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        current_user.phone_number = form.phone_number.data
        current_user.ID_number = form.id_number.data
        current_user.next_of_kin = form.next_of_kin.data
        current_user.next_of_kin_phone_number = form.next_of_kin_phone_number.data
        current_user.address = form.address.data
        db.session.commit()
        flash("Your account has been updated", 'success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        # populate the form fields with the users details
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name
        form.phone_number.data = current_user.phone_number
        form.id_number.data = current_user.ID_number
        form.next_of_kin.data = current_user.next_of_kin
        form.next_of_kin_phone_number.data = current_user.next_of_kin_phone_number
        form.address.data = current_user.address
    image_file = url_for('static', filename=f'media/profile_pics/{current_user.image_file}')
    return render_template('account.html', title=f"{current_user.username} account", image_file=image_file, form=form)


@users.route("/pending-accounts", methods=['GET', 'POST'])
@login_required
def pending_accounts():
    inactive_users = User.query.filter_by(active=False).all()
    # print(inactive_users)
    user_image_paths = []
    for user in inactive_users:
        i = {
            "username": user.username,
            "image_path": url_for('static', filename=f'media/profile_pics/{user.image_file}')
        }
        user_image_paths.append(i)
    return render_template('pending_accounts.html', users=inactive_users, images=user_image_paths)


@users.route("/pending-accounts/<int:user_id>", methods=["GET", "POST"])
@login_required
def activate_pending_account(user_id):
    form = ActiveAccountForm()
    user = User.query.filter_by(id=user_id).first()
    if form.validate_on_submit():
        user.active = form.active.data
        db.session.commit()
        if form.active.data:
            flash(f"{user.email}'s account has been activated", 'success')
        if not form.active.data:
            flash(f"{user.email}'s account has not been activated", 'warning')
        return redirect(url_for("users.pending_accounts"))
    return render_template('activate_account.html', form=form, user=user)
