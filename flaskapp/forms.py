from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, SubmitField, SelectField, IntegerField, DateField, RadioField, SelectMultipleField, \
    PasswordField, FileField, BooleanField
from wtforms.validators import DataRequired, NumberRange, ValidationError


class SignUpForm(FlaskForm):
    first_name = StringField('First name*:', validators=[DataRequired()])
    last_name = StringField('Last name*:', validators=[DataRequired()])
    email = StringField('Email address*:', validators=[DataRequired()])
    password = PasswordField('Password*:', validators=[DataRequired()])
    password2 = PasswordField('Confirm Password*:', validators=[DataRequired()])
    submit = SubmitField('Sign Up')


class EditProfileForm(FlaskForm):
    birthday = DateField('Date of Birth', validators=[DataRequired()])
    marital_status = RadioField('Marital Status', choices=[('Single', 'Single'), ('Married', 'Married')])
    gender = RadioField('Gender', choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')])
    city = StringField('City', validators=[DataRequired()])
    country = StringField('Country', validators=[DataRequired()])
    traveled_countries = StringField('Previously Traveled Countries', validators=[DataRequired()])
    profile_picture = FileField('Profile Picture',
                                validators=[FileAllowed(['jpg'], message="Only .jpg files are accepted")])
    submit = SubmitField('Save Profile')


class LoginForm(FlaskForm):
    email = StringField('Email address*:', validators=[DataRequired()])
    password = PasswordField('Password*:', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class TravelReservationForm(FlaskForm):
    package = SelectField('Select Tour Package*',
                          choices=[('China', 'China'), ('India', 'India'), ('Europe', 'Europe'), ('USA', 'USA')],
                          validators=[DataRequired()])
    arrival_date = DateField('Arrival date*:', validators=[DataRequired()])
    num_of_people = IntegerField('Number of people*:', validators=[DataRequired(), NumberRange(min=5, max=20)])
    facilities = SelectMultipleField('Facilities Needed?',
                                     choices=[('Boarding', 'Boarding'), ('Sight seeing', 'Sight seeing')])
    discount_coupon_used = StringField('Discount Coupon code:')
    agree_terms = RadioField('Terms and Conditions*', choices=[('I agree', 'I agree'), ('I disagree', 'I disagree')],
                             validators=[DataRequired()])
    submit = SubmitField('Complete reservation')

    def validate_discount_code(form, field):
        if field.data:
            valid_codes = ['TRVL2435', 'TRVL4657', 'TRVL6879']
            if field.data not in valid_codes:
                raise ValidationError('Invalid discount code.')
