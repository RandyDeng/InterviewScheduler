from flask import redirect, render_template

from app.login.user_login_manager import valid_applicant, first_login

from . import user


@user.route('/<string:id>', methods=['GET'])
@user.route('/dashboard/<string:id>', methods=['GET'])
def dashboard(id):
    if first_login(id, flashing=False):
        return redirect('/login/' + id)
    if not valid_applicant(id, flashing=True):
        return redirect('/login/user')
    return render_template('user_dashboard.html', user_id=id)


@user.route('/interviews/<string:id>', methods=['GET'])
def documentation(id):
    if first_login(id, flashing=False):
        return redirect('/login/' + id)
    if not valid_applicant(id, flashing=True):
        return redirect('/login/user')
    return render_template('user_interviews.html', user_id=id)
