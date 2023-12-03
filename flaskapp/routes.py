from flask import render_template, flash, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from flaskapp import app, db
from flaskapp.forms import TravelReservationForm, SignUpForm, EditProfileForm, SignInForm
from flaskapp.models import User, Reservation, Profile
from flaskapp.config import Config
import os


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():  # 如果用户提交的数据通过了所有的验证器
        # 判断用户输入的邮箱是否已经存在
        if User.query.filter(User.email == form.email.data).first():
            flash('User already exists with email: {}'.format(form.email.data))
            return redirect(url_for('signup'))
        # 判断两次输入的密码是否一致
        if form.password.data != form.password2.data:
            flash('Password do not match!')
            return redirect(url_for('signup'))
        passw_hash = generate_password_hash(form.password.data)
        user = User(first_name=form.first_name.data, last_name=form.last_name.data, email=form.email.data,
                    password_hash=passw_hash)
        db.session.add(user)
        db.session.commit()
        session['ID'] = user.id
        flash('Sign Up success!')
        return redirect(url_for('edit_profile'))
    return render_template('signup.html', title='Sign Up', form=form)


@app.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    form = EditProfileForm()
    if not session.get('ID') is None:
        # get the user object from the database
        user_in_db = User.query.filter(User.id == session.get('ID')).first()
        if form.validate_on_submit():
            profile_picture_dir = Config.JPG_UPLOAD_DIR
            file_obj = form.profile_picture.data
            print(file_obj)
            profile_picture_filename = user_in_db.first_name + '_profile_picture.jpg'
            file_obj.save(os.path.join(profile_picture_dir, profile_picture_filename))
            flash('Profile picture uploaded and saved')
            # check if user already has a profile
            stored_profile = Profile.query.filter(Profile.user == user_in_db).first()
            if not stored_profile:
                # if no profile exists, add a new object
                profile = Profile(birthday=form.birthday.data, marital_status=form.marital_status.data,
                                  gender=form.gender.data, city=form.city.data, country=form.country.data,
                                  traveled_countries=form.traveled_countries.data,
                                  profile_picture=profile_picture_filename, user=user_in_db)
                db.session.add(profile)
            else:
                # else, modify the existing object with form data
                stored_profile.birthday = form.birthday.data
                stored_profile.marital_status = form.marital_status.data
                stored_profile.gender = form.gender.data
                stored_profile.city = form.city.data
                stored_profile.country = form.country.data
                stored_profile.traveled_countries = form.traveled_countries.data
            db.session.commit()
            return redirect(url_for('profile'))
        else:
            stored_profile = Profile.query.filter(Profile.user == user_in_db).first()
            if not stored_profile:
                return render_template('edit_profile.html', title='Add your Profile', form=form)
            else:
                form.birthday.data = stored_profile.birthday
                form.marital_status.data = stored_profile.marital_status
                form.gender.data = stored_profile.gender
                form.city.data = stored_profile.city
                form.country.data = stored_profile.country
                form.traveled_countries.data = stored_profile.traveled_countries
                return render_template('edit_profile.html', title='Modify your Profile', form=form)
    else:
        flash('Please sign up first')
        return redirect(url_for('signup'))


@app.route('/signin', methods=['GET', 'POST'])
def signin():
    form = SignInForm()
    if form.validate_on_submit():
        user_in_db = User.query.filter(User.email == form.email.data).first()
        if not user_in_db:
            flash('No user found with email: {}, please signup or retry with a valid email'.format(form.email.data))
            return redirect(url_for('signin'))
        if user_in_db and check_password_hash(user_in_db.password_hash, form.password.data):
            flash('Login success!')
            session['ID'] = user_in_db.id
            return redirect(url_for('profile'))
        flash('Incorrect Password, please reenter your password')
        return redirect(url_for('signin'))
    return render_template('signin.html', title='Sign In', form=form)


@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if session.get('ID') is None:
        flash('Please sign up first')
        return redirect(url_for('signup'))
    user_in_db = User.query.filter(User.id == session.get('ID')).first()
    reservations = None
    if user_in_db:
        reservations = Reservation.query.filter(Reservation.user_id == user_in_db.id).all()
    return render_template('profile.html', title='Profile', user=user_in_db, reservations=reservations)


@app.route('/form', methods=['POST', 'GET'])
def form():
    form = TravelReservationForm()
    if form.validate_on_submit():
        if form.agree_terms.data != 'I agree':
            flash(
                'The reservation failed. Please agree to the terms and conditions to successfully make a reservation.')
            return redirect(url_for('form'))

        reservation = Reservation(
            package=form.package.data,
            arrival_date=form.arrival_date.data,
            num_of_people=form.num_of_people.data,
            boarding='Boarding' in form.facilities.data,
            sight_seeing='Sight seeing' in form.facilities.data,
            discount_coupon_used=bool(form.discount_coupon_used.data)
        )
        db.session.add(reservation)
        db.session.commit()

        flash('Reservation Complete!')
        return redirect(url_for('form'))
    return render_template('form.html', title='Travel Reservation Form', form=form)


@app.route('/logout')
def logout():
    session.pop("ID", None)
    return redirect(url_for('index'))
