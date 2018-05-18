from flask_wtf import FlaskForm
from flask_wtf.file import FileField

from wtforms import (PasswordField, SelectField, SelectMultipleField,
                     StringField, SubmitField,
                     TextAreaField, widgets)
from wtforms.fields.html5 import DateField, EmailField
from wtforms.validators import InputRequired, Length, Regexp, ValidationError

from app.utils.environment import next_semesters, positions


class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class AdminForm(FlaskForm):
    username = StringField('Username', validators=[
                                InputRequired("Please enter your username"),
                                Length(min=1, max=50)],
                           render_kw={"placeholder": "Username"})
    password = PasswordField('Password', validators=[
                                InputRequired("Please enter your password"),
                                Length(min=1, max=50)],
                             render_kw={"placeholder": "Password"})
    submit = SubmitField("Login")


class UserForm(FlaskForm):
    first_name = StringField('First Name', validators=[
                                InputRequired("Please enter your first name"),
                                Length(min=1, max=50),
                                Regexp('^[a-zA-Z]*$')],
                             render_kw={"placeholder": "First Name"})
    last_name = StringField('Last Name', validators=[
                                InputRequired(),
                                Length(min=1, max=50),
                                Regexp('^[a-zA-Z]*$')],
                            render_kw={"placeholder": "Last Name"})
    email = EmailField('Georgia Tech Email', validators=[
                            InputRequired(),
                            Length(min=1, max=50)],
                       render_kw={"placeholder": "Georgia Tech Email"})
    position = SelectField('Position you are applying for:', choices=[
                            (positions['PI'], positions['PI']),
                            (positions['President'], positions['President']),
                            (positions['VP'], positions['VP']),
                            (positions['DoF'], positions['DoF']),
                            (positions['DoO'], positions['DoO']),
                            (positions['DoC'], positions['DoC']),
                            (positions['DoN'], positions['DoN'])])
    submit = SubmitField("Begin Registration")

    def validate_email(form, field):
        if not field.data.endswith('@gatech.edu'):
            raise ValidationError('Email must be valid Georgia Tech Email')


class OfficerRegistrationForm(FlaskForm):
    first_name = StringField(render_kw={"disabled": True})
    last_name = StringField(render_kw={"disabled": True})
    email = EmailField(render_kw={"disabled": True})
    position = StringField(render_kw={"disabled": True})
    phone_number = StringField('Phone Number:', validators=[
                                InputRequired(),
                                Length(min=1, max=50)],
                               render_kw={'placeholder': "Phone Number"})
    year = SelectField('Select your year:', choices=[
                        ('1st', '1st Year'),
                        ('2nd', '2nd Year'),
                        ('3rd', '3rd Year'),
                        ('4th', '4th Year'),
                        ('5+', '5+ Years'),
                        ('Master', 'Master'),
                        ('PhD', 'PhD'),
                        ('Other', 'Other')])
    expected_graduation_date = DateField('Expected Graduation Date:',
                                         validators=[InputRequired()],
                                         render_kw={"pattern":
                                                    "[0-9]{2}-[0-9]{2}[0-9]{4}"
                                                    })
    semesters = [(s, s) for s in next_semesters()]
    on_campus = MultiCheckboxField('Please check which semesters you will be '
                                   'on campus:', choices=semesters)
    why_interested = TextAreaField('Why are you interested in this position?',
                                   validators=[InputRequired(),
                                               Length(max=10000)])
    comments = TextAreaField('Additional comments/concerns:',
                             validators=[InputRequired(), Length(max=10000)])
    resume = FileField('Upload Resume (1MB limit, *.pdf only):')
    skills = TextAreaField('List 3-5 skills that make you qualified '
                           'for this position:',
                           validators=[InputRequired(), Length(max=10000)])
    submit = SubmitField("Complete Registration")


class PIRegistrationForm(FlaskForm):
    first_name = StringField(render_kw={"disabled": True})
    last_name = StringField(render_kw={"disabled": True})
    email = EmailField(render_kw={"disabled": True})
    position = StringField(render_kw={"disabled": True})
    phone_number = StringField('Phone Number:', validators=[
                                InputRequired(),
                                Length(min=1, max=50)],
                               render_kw={'placeholder': "Phone Number"})
    year = SelectField('Select your year:', choices=[
                        ('1st', '1st Year'),
                        ('2nd', '2nd Year'),
                        ('3rd', '3rd Year'),
                        ('4th', '4th Year'),
                        ('5+', '5+ Years'),
                        ('Master', 'Master'),
                        ('PhD', 'PhD'),
                        ('Other', 'Other')])
    expected_graduation_date = DateField('Expected Graduation Date:',
                                         validators=[InputRequired()],
                                         render_kw={"pattern":
                                                    "[0-9]{2}-[0-9]{2}[0-9]{4}"
                                                    })
    semesters = [(s, s) for s in next_semesters()]
    on_campus = MultiCheckboxField('Please check which semesters you will be '
                                   'on campus:', choices=semesters)
    why_interested = TextAreaField('Why are you interested in this position?',
                                   validators=[InputRequired(),
                                               Length(max=10000)])
    comments = TextAreaField('Additional comments/concerns:',
                             validators=[InputRequired(), Length(max=10000)])
    resume = FileField('Upload Resume (1MB limit, *.pdf only):')
    submit = SubmitField("Complete Registration")
