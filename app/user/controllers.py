from flask import abort, redirect, render_template, url_for

from app.login.user_login_manager import valid_applicant

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
    return render_template('user_dashboard.html', user_id=id)


@user.route('/interviews/<string:id>', methods=['GET'])
def documentation(id):
    if not valid_applicant(id):
        abort(404)
    return render_template('user_interviews.html', user_id=id)
