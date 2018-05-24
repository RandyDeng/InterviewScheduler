from flask import flash

from flask_wtf import FlaskForm

from wtforms import PasswordField, SelectField, StringField, SubmitField

from app.utils.environment import POSITIONS
from app.login.admin_login_manager import verify_credentials
from app.login.forms import MultiCheckboxField


# Flask Forms: This section contains all of the forms used
# inside the login blueprint. Included are login forms and
# user registration forms.
class UpdatePasswordForm(FlaskForm):
    username = StringField(
        'Current Username',
        render_kw={"placeholder": "Current Username"})
    password = PasswordField(
        'Current Password',
        render_kw={"placeholder": "Current Password"})
    new_password = PasswordField(
        'New Password',
        render_kw={"placeholder": "New Password"})
    new_password_copy = PasswordField(
        'Confirm New Password',
        render_kw={"placeholder": "Confirm New Password"})
    submit = SubmitField("Update Password")

    def validate(self):
        if (not self.username.data) or (not self.password.data):
            flash('You may not leave the username and password empty',
                  'alert alert-danger')
            return False
        if ((not self.new_password.data) or
           (not self.new_password_copy.data)):
            flash('Your new password may not be empty', 'alert alert-danger')
            return False
        if not verify_credentials(self.username.data, self.password.data):
            flash('The password you entered is incorrect',
                  'alert alert-danger')
            return False
        if not self.new_password.data == self.new_password_copy.data:
            flash('Your new password does not match', 'alert alert-danger')
            return False
        return True


class AvailablePositionsForm(FlaskForm):
    available_positions = MultiCheckboxField(
        'Check the positions you would like available:',
        choices=[(value, value) for key, value in POSITIONS.items()])
    position_submit = SubmitField('Update Available Positions')


class DeleteUnverifiedUsersForm(FlaskForm):
    submit = SubmitField('Delete All Unverified Applicants')


class InterviewSchedulerForm(FlaskForm):
    dates = StringField(
        'Enter interview dates using MM/DD/YYYY format:',
        render_kw={'placeholder': 'e.g.: 03/02/2018;03/04/2018'})
    length = SelectField(
        'Length of each time slot:',
        choices=[('30', '30 minutes'), ('60', '60 minutes')])
    submit = SubmitField('Add Availability')
