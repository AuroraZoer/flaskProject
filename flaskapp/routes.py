from flask import render_template, flash, redirect, url_for, session

from flaskapp import app, db
from flaskapp.forms import travelReservationForm, historyForm
from flaskapp.models import User, Reservation


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home')


@app.route('/form', methods=['POST', 'GET'])
def form():
    form = travelReservationForm()
    if form.validate_on_submit():
        if form.agree_terms.data != 'I agree':
            flash(
                'The reservation failed. Please agree to the terms and conditions to successfully make a reservation.')
            return redirect(url_for('form'))

        user = User.query.filter(User.email == form.email.data).first()
        if not user:
            user = User(full_name=form.full_name.data, email=form.email.data)
            db.session.add(user)
            db.session.commit()

        reservation = Reservation(
            user_email=form.email.data,
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


@app.route('/history', methods=['GET', 'POST'])
def history():
    form = historyForm()
    reservations = None
    user = None
    if form.validate_on_submit():
        user = User.query.filter(User.email == form.email.data).first()
        if user:
            reservations = Reservation.query.filter(Reservation.user_email == form.email.data).all()
        else:
            flash('No user found with email: {}'.format(form.email.data))
            return redirect(url_for('history'))
    return render_template('history.html', title='Reservation History', form=form, reservations=reservations, user=user)