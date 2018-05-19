import datetime
import humanize
import os
import phonenumbers
import re

from flask import flash

from flask_wtf import FlaskForm
from flask_wtf.file import FileField

from wtforms import (PasswordField, SelectField, SelectMultipleField,
                     StringField, SubmitField,
                     TextAreaField, widgets)
from wtforms.fields.html5 import DateField, EmailField
from wtforms.validators import InputRequired, Length, ValidationError

from app.utils.environment import next_semesters, positions


# Custom validators: This section contains all custom validators
# for the forms. Custom validators have the option of using flask
# to flash a message to the user. However, keep in mind that these
# messages assume a specific format to work and that other messages
# from the controller files may also appear.
def check_name(message, min=1, max=25):
    message = message.format(min, max)

    def _check_name(form, field):
        pattern = '^[a-zA-Z]*$'
        if not ((min <= len(field.data) <= max) and
                re.match(pattern, field.data)):
            flash(message, 'alert alert-danger')
            raise ValidationError(message)
    return _check_name


def check_gt_email(message, min=12, max=50):
    message = message.format(min, max)

    def _check_gt_email(form, field):
        if not ((min <= len(field.data) <= max) or
                field.data.endswith('@gatech.edu')):
                    flash(message, 'alert alert-danger')
                    raise ValidationError(message)
    return _check_gt_email


def check_phone_number(message):
    def _check_phone_number(form, field):
        if len(field.data) > 16:
            flash(message, 'alert alert-danger')
            raise ValidationError(message)
        try:
            input_number = phonenumbers.parse(field.data)
            if not (phonenumbers.is_valid_number(input_number)):
                pass
        except phonenumbers.phonenumberutil.NumberParseException:
            try:
                input_number = phonenumbers.parse("+1"+field.data)
                if not (phonenumbers.is_valid_number(input_number)):
                    flash(message, 'alert alert-danger')
                    raise ValidationError(message)
            except phonenumbers.phonenumberutil.NumberParseException:
                flash(message, 'alert alert-danger')
                raise ValidationError(message)

        field.data = phonenumbers.format_number(
            input_number,
            phonenumbers.PhoneNumberFormat.INTERNATIONAL)
    return _check_phone_number


def check_date(message):
    def _check_date(form, field):
        if not isinstance(field.data, datetime.date):
            flash(message, 'alert alert-danger')
            raise ValidationError(message)
    return _check_date


def check_open_ended(message, max):
    message = message.format(humanize.intcomma(max))

    def _check_open_ended(form, field):
        if len(field.data) > max:
            flash(message, 'alert alert-danger')
            raise ValidationError(message)
    return _check_open_ended


def check_upload():
    message_1 = 'You must upload your resume'
    message_2 = 'The file must be in .pdf format'
    message_3 = 'Your file has exceeded 1MB in size'
    max = 1024*1024  # max=8MB

    def _check_upload(form, field):
        if field.data is None:
            flash(message_1, 'alert alert-danger')
            raise ValidationError(message_1)
        if not (os.path.splitext(field.data.filename)[1] == '.pdf'):
            flash(message_2, 'alert alert-danger')
            raise ValidationError(message_2)
        field.data.seek(0, os.SEEK_END)
        size = field.data.tell()
        field.data.seek(0)
        if size > max:
            flash(message_3, 'alert alert-danger')
            raise ValidationError(message_3)
    return _check_upload


# Flask Forms: This section contains all of the forms used
# inside the login blueprint. Included are login forms and
# user registration forms.
class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class AdminForm(FlaskForm):
    username = StringField(
        'Username',
        validators=[
            InputRequired("Please enter your username"),
            Length(min=1, max=50)],
        render_kw={"placeholder": "Username"})
    password = PasswordField(
        'Password',
        validators=[
            InputRequired("Please enter your password"),
            Length(min=1, max=50)],
        render_kw={"placeholder": "Password"})
    submit = SubmitField("Login")


class UserForm(FlaskForm):
    first_name = StringField(
        'First Name',
        validators=[check_name(
            'First names must be between {} and {} '
            'characters long and contain only letters')],
        render_kw={"placeholder": "First Name"})
    last_name = StringField(
        'Last Name',
        validators=[check_name(
            'Last names must be between {} and {} '
            'characters long and contain only letters')],
        render_kw={"placeholder": "Last Name"})
    email = EmailField(
        'Georgia Tech Email',
        validators=[check_gt_email(
            'Emails must be a valid GT email between '
            '{} and {} characters long')],
        render_kw={"placeholder": "Georgia Tech Email"})
    position = SelectField(
        'Position you are applying for:', choices=[
            (positions['PI'], positions['PI']),
            (positions['President'], positions['President']),
            (positions['VP'], positions['VP']),
            (positions['DoF'], positions['DoF']),
            (positions['DoO'], positions['DoO']),
            (positions['DoC'], positions['DoC']),
            (positions['DoN'], positions['DoN'])])
    submit = SubmitField("Begin Registration")


class RegistrationForm(FlaskForm):
    # General questions (PIs only answer general questions)
    first_name = StringField(render_kw={"disabled": True})
    last_name = StringField(render_kw={"disabled": True})
    email = EmailField(render_kw={"disabled": True})
    position = StringField(render_kw={"disabled": True})
    phone_number = StringField(
        'Phone Number:',
        validators=[check_phone_number('Please enter a valid phone number')],
        render_kw={'placeholder': "Phone Number"})
    year = SelectField(
        'Select your year:',
        choices=[
            ('1st', '1st Year'),
            ('2nd', '2nd Year'),
            ('3rd', '3rd Year'),
            ('4th', '4th Year'),
            ('5+', '5+ Years'),
            ('Master', 'Master'),
            ('PhD', 'PhD'),
            ('Other', 'Other')])
    expected_graduation_date = DateField(
        'Expected Graduation Date:',
        validators=[check_date('Please enter a valid graduation date')],
        render_kw={'pattern': '[0-9]{2}/[0-9]{2}/[0-9]{4}'})
    on_campus = MultiCheckboxField(
        'Please check which semesters you will be on campus:',
        choices=[(s, s) for s in next_semesters()])
    why_interested = TextAreaField(
        'Why are you interested in this position?',
        validators=[check_open_ended(
            'Your response to `Why are you interested in this position?`'
            ' has exceeded the {} character limit',
            max=10000)])
    comments = TextAreaField(
        'Additional comments/concerns:',
        validators=[check_open_ended(
            'Your response to `Additional comments/concerns`'
            ' has exceeded the {} character limit',
            max=10000)])
    resume = FileField(
        'Upload Resume (1MB limit, *.pdf only):',
        validators=[check_upload()])
    submit = SubmitField("Complete Registration")

    #  Officer specific questions
    skills = TextAreaField(
        'List 3-5 skills that make you qualified for this position:',
        validators=[check_open_ended(
            'Your response to `List 3-5 skills`'
            ' has exceeded the {} character limit',
            max=10000)])
