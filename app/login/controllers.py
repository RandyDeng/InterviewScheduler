from flask import abort, flash, request, redirect, render_template, url_for
from flask_login import login_user, logout_user

from app.utils import environment, mailer, mongo

from . import forms, login, admin_login_manager, user_login_manager


def application_link_generator(id):
    return (environment.ENV_VARIABLES['BASE_URL'] + 'user/' + id)


@login.route('/<string:id>', methods=['GET'])
def route(id):
    if user_login_manager.first_login(id):
        return redirect(url_for('.registration', id=id))
    if user_login_manager.valid_applicant(id):
        return redirect(url_for('user.route', id=id))
    return redirect(url_for('.user'))


@login.route('/admin', methods=['GET', 'POST'])
def admin():
    logout_user()
    form = forms.AdminForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            if (admin_login_manager.verify_credentials(
                    form.username.data, form.password.data)):
                user = admin_login_manager.User(form.username.data)
                login_user(user)
                return redirect(url_for('admin.dashboard'))
        flash('Invalid username and password', 'alert alert-danger')
    return render_template('admin.html', form=form)


@login.route('/user', methods=['GET', 'POST'])
def user():
    form = forms.UserForm()
    try:
        choices = [(p, p) for p in mongo.AvailablePositions.objects.first()[
                    'available_positions']]
    except BaseException:
        mongo.AvailablePositions(available_positions=[]).save()
        choices = []
    if not choices:
        choices = [('No positions available', 'No positions available')]
    form.position.choices = choices
    if (request.method == 'POST'):
        if form.validate_on_submit():
            kwargs = {
                'email': form.email.data,
                'first_name': form.first_name.data,
                'last_name': form.last_name.data,
                'position': form.position.data
            }
            unverified_user = mongo.unverified_user_generator(**kwargs)
            unverified_user.save()
            mailer.send_email_template(
                form.email.data,
                'email_verification',
                {
                    'first_name': form.first_name.data,
                    'application_link': application_link_generator(
                        unverified_user.user_id),
                    'position': form.position.data
                }
            )
            flash('Registration sent!', 'alert alert-success')
            return redirect(url_for('.email_verification'))
    return render_template('user.html', form=form)


@login.route('/email_verification', methods=['GET'])
def email_verification():
    return render_template('email_verification.html')


@login.route('/registration/<string:id>', methods=['GET', 'POST'])
def registration(id):
    if not user_login_manager.first_login(id):
        abort(404)

    form = forms.RegistrationForm()
    unverified_id = mongo.UnverifiedUser.objects().get(user_id=id)
    if request.method == 'POST':
        if form.validate_on_submit():
            new_app = mongo.Applicant(
                user_id=id,
                first_name=unverified_id.first_name,
                last_name=unverified_id.last_name,
                email=unverified_id.email,
                position=unverified_id.position,
                phone_number=form.phone_number.data,
                year=form.year.data,
                expected_graduation_date=form.expected_graduation_date.data,
                on_campus=', '.join(form.on_campus.data),
                why_interested=form.why_interested.data,
                comments=form.comments.data,
                resume=bytes(form.resume.data.read())
            )

            if not unverified_id.position == environment.POSITIONS['PI']:
                new_app.skills = form.skills.data

            new_app.save()
            unverified_id.delete()
            return redirect(url_for('user.route', id=id))
    if unverified_id.position == environment.POSITIONS['PI']:
        return render_template('pi_registration.html', user_id=id, form=form,
                               user=unverified_id)
    else:
        return render_template('officer_registration.html', user_id=id,
                               form=form, user=unverified_id)
