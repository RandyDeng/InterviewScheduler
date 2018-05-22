from flask import abort, redirect, render_template, url_for

from app.login.user_login_manager import valid_applicant
from app.utils.mongo import Applicant

from . import user


@user.route('/<string:id>', methods=['GET'])
def route(id):
    if valid_applicant(id):
        return redirect(url_for('.dashboard', id=id))
    else:
        return redirect(url_for('login.route', id=id))


@user.route('/dashboard/<string:id>', methods=['GET'])
def dashboard(id):
    if not valid_applicant(id):
        abort(404)
    applicant = Applicant.objects().get(user_id=id)
    return render_template('user_dashboard.html', applicant=applicant)


@user.route('/interviews/<string:id>', methods=['GET'])
def interviews(id):
    if not valid_applicant(id):
        abort(404)
    applicant = Applicant.objects().get(user_id=id)
    return render_template('user_interviews.html', applicant=applicant)
