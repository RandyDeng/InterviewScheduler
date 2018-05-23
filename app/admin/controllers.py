import json
import urllib

from flask import (abort, make_response, redirect,
                   flash, render_template, request)
from flask_login import login_required
from werkzeug import generate_password_hash

from app.utils import environment, mongo

from .forms import UpdatePasswordForm
from . import admin, query


@admin.route('/logout', methods=['GET'])
def logout():
    return redirect('login/admin')


@admin.route('/', methods=['GET'])
@admin.route('/dashboard', methods=['GET'])
@login_required
def dashboard():
    kwargs = {
        'current_applications': mongo.Applicant.objects(
            semester=environment.current_semester()).count(),
        'total_applications': mongo.Applicant.objects.count(),
        'all_unverified': mongo.UnverifiedUser.objects.count(),
    }
    kwargs.update(query.get_kwargs())
    return render_template('dashboard.html', **kwargs)


@admin.route('/control_panel', methods=['GET', 'POST'])
@login_required
def control_panel():
    password_form = UpdatePasswordForm()
    if request.method == 'POST':
        if password_form.validate_on_submit():
            admin = mongo.Admins.objects.get(
                username=password_form.username.data)
            admin.password = generate_password_hash(
                password_form.new_password.data)
            admin.save()
            flash('Password has been updated successfully!',
                  'alert alert-success')
    return render_template('control_panel.html', password_form=password_form)


@admin.route('/applications', methods=['GET'])
@login_required
def applications():
    return render_template('applications.html', **query.get_kwargs())


@admin.route('/applications/<string:urlquery>', methods=['GET'])
@login_required
def applications_query(urlquery):
    urlquery = json.loads(urllib.parse.unquote(urlquery))
    title = urlquery['title']
    mongo_object = urlquery['mongo_object']
    color = urlquery['color']
    query = urlquery['query']
    if mongo_object == 'Applicant':
        applicants = mongo.Applicant.objects(__raw__=query)
        return render_template('applications_query_applicant_list.html',
                               title=title,
                               color=color,
                               applicants=applicants)
    elif mongo_object == 'UnverifiedUser':
        unverified_users = mongo.UnverifiedUser.objects(__raw__=query)
        return render_template('applications_query_unverified_list.html',
                               title=title,
                               color=color,
                               unverified_users=unverified_users)


@admin.route('/applications/applicant/<string:id>', methods=['GET'])
@login_required
def applications_applicant(id):
    try:
        applicant = mongo.Applicant.objects().get(user_id=id)
        if 'PENDING' in applicant.status:
            color = 'orange'
        elif 'REJECTION' in applicant.status:
            color = 'red'
        elif 'ACCEPTANCE' in applicant.status:
            color = 'green'
        return render_template('applications_applicant.html',
                               applicant=applicant,
                               color=color)
    except (mongo.Applicant.DoesNotExist,
            mongo.Applicant.MultipleObjectsReturned):
        abort(500)


@admin.route('/applications/resume/<string:id>',
             methods=['GET'])
@login_required
def applications_resume(id):
    try:
        applicant = mongo.Applicant.objects().get(user_id=id)
    except (mongo.Applicant.DoesNotExist,
            mongo.Applicant.MultipleObjectsReturned):
        abort(500)

    binary_pdf = applicant.resume
    response = make_response(binary_pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = \
        'inline; filename=%s.pdf' % (applicant.first_name +
                                     '_' + applicant.last_name + '_resume')
    return response


@admin.route('/applications/decision/<string:decision>/<string:id>',
             methods=['GET'])
@login_required
def applications_decision(decision, id):
    try:
        applicant = mongo.Applicant.objects().get(user_id=id)
    except (mongo.Applicant.DoesNotExist,
            mongo.Applicant.MultipleObjectsReturned):
        abort(500)

    if applicant.status == mongo.APPLICANT_STATUS[0]:
        if decision == 'accept':
            applicant.status == mongo.APPLICANT_STATUS[2]
        elif decision == 'reject':
            applicant.status == mongo.APPLICANT_STATUS[1]

    elif applicant.status == mongo.APPLICANT_STATUS[2]:
        if decision == 'accept':
            if applicant.position == 'Peer Instructor':
                applicant.status == mongo.APPLICANT_STATUS[6]
            else:
                applicant.status == mongo.APPLICANT_STATUS[4]
        elif decision == 'reject':
            applicant.status == mongo.APPLICANT_STATUS[3]

    elif applicant.status == mongo.APPLICANT_STATUS[4]:
        if decision == 'accept':
            applicant.status == mongo.APPLICANT_STATUS[6]
        elif decision == 'reject':
            applicant.status == mongo.APPLICANT_STATUS[5]
    return redirect('/admin/applications/applicant/' + id)


@admin.route('/interview_scheduler', methods=['GET', 'POST'])
@login_required
def interview_scheduler():
    return render_template('interview_scheduler.html')


@admin.route('/history', methods=['GET'])
@login_required
def history():
    return render_template('history.html')


@admin.route('/devs', methods=['GET'])
@login_required
def devs():
    return render_template('devs.html')


@admin.route('/documentation', methods=['GET'])
@login_required
def documentation():
    return render_template('documentation.html')
