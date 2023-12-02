from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, IntegerField, DateField, RadioField, SelectMultipleField
from wtforms.validators import DataRequired, NumberRange, ValidationError


class travelReservationForm(FlaskForm):
    full_name = StringField('Full name*:', validators=[DataRequired()])
    email = StringField('Email address*:', validators=[DataRequired()])
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


class historyForm(FlaskForm):
    email = StringField('Email address*:', validators=[DataRequired()])
    submit = SubmitField('Search')
