import json
import urllib

from flask import (abort, make_response, redirect, flash,
                   render_template, request, session, url_for)
from flask_login import login_required
from werkzeug import generate_password_hash

from app.utils import environment, mongo

from . import admin, forms, interview_scheduler, query


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
    position_form = forms.AvailablePositionsForm()
    password_form = forms.UpdatePasswordForm()
    flash_message = None
    if request.method == 'POST':
        if position_form.position_submit.data:
            flash_message = 'position'
            if position_form.validate_on_submit():
                p_list = mongo.AvailablePositions.objects().first()
                p_list.available_positions = (
                    position_form.available_positions.data)
                p_list.save()
                flash('Available positions has been updated successfully!',
                      'alert alert-success')
        if password_form.submit.data:
            flash_message = 'password'
            if password_form.validate_on_submit():
                admin = mongo.Admins.objects.get(
                    username=password_form.username.data)
                admin.update(set__password=generate_password_hash(
                    password_form.new_password.data))
                flash('Password has been updated successfully!',
                      'alert alert-success')
    # Only one entry should exist in the AvailablePositions Document
    try:
        p_list = mongo.AvailablePositions.objects().first()[
            'available_positions']
    except BaseException:
        mongo.AvailablePositions(available_positions=[]).save()
        p_list = []
    return render_template('control_panel.html',
                           position_form=position_form,
                           password_form=password_form,
                           p_list=p_list,
                           flash_message=flash_message)


@admin.route('/applications', methods=['GET'])
@login_required
def applications():
    return render_template('applications.html', **query.get_kwargs())


@admin.route('/applications/<string:urlquery>', methods=['GET', 'POST'])
@login_required
def applications_query(urlquery):
    urlquery = json.loads(urllib.parse.unquote(urlquery))
    mongo_object = urlquery['mongo_object']
    raw_query = urlquery['query']
    if mongo_object == 'Applicant':
        urlquery['applicants'] = mongo.Applicant.objects(__raw__=raw_query)
        return render_template(
            'applications_query_applicant_list.html', **urlquery)
    elif mongo_object == 'UnverifiedUser':
        form = forms.DeleteUnverifiedUsersForm()
        if request.method == 'POST':
            if form.validate_on_submit():
                mongo.UnverifiedUser.objects.delete()
                flash('All unverified users have been successfully deleted',
                      'alert alert-success')
        urlquery['form'] = form
        urlquery['unverified_users'] = mongo.UnverifiedUser.objects(
            __raw__=raw_query)
        urlquery.update(query.get_kwargs())
        return render_template('applications_query_unverified_list.html',
                               **urlquery)


@admin.route('/applications/applicant/<string:id>', methods=['GET', 'POST'])
@login_required
def applications_applicant(id):
    try:
        applicant = mongo.Applicant.objects().get(user_id=id)
    except (mongo.Applicant.DoesNotExist,
            mongo.Applicant.MultipleObjectsReturned):
        abort(500)

    form = forms.ApplicationDecisionsForm()
    if request.method == 'POST' and form.validate_on_submit():
        new_status = mongo.next_status(applicant, form.accept.data)
        applicant.update(set__status=new_status)
        applicant.status = new_status
        if new_status == applicant.status:
            flash('No more decisions may be made for this applicant',
                  'alert alert-danger')
        else:
            flash('Decision has been submitted', 'alert alert-success')
    return render_template('applications_applicant.html',
                           applicant=applicant,
                           form=form,
                           APPLICANT_STATUS=mongo.APPLICANT_STATUS)


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


@admin.route('/interview_scheduler', methods=['GET', 'POST'])
@admin.route('/interview_scheduler/step/<int:step>', methods=['GET', 'POST'])
@login_required
def interviewscheduler(step=1):
    kwargs = {'step': step}
    if step is 0:
        interview_scheduler.clean_session()
        kwargs['step'] = kwargs['step'] + 1
    elif step is 1:
        form = forms.InterviewSchedulerForm()
        if request.method == 'POST':
            if form.validate_on_submit():
                session[interview_scheduler.SESSION_METADATA] = json.dumps(
                    {
                        'dates': form.dates.data.replace(' ', ''),
                        'length': form.length.data,
                        'committee_size': form.committee_size.data,
                        'match_position': form.match_position.data
                    }
                )
                return redirect(url_for('.interviewscheduler', step=2))
    elif step is 2:
        # TODO split the dates
        # TODO generate multipart form with each of the dates
        # TODO add another button to add another person which will redirect to step 2 again
        # TODO associate a persons name and position
        # retrieve info from step 1 and store in kwargs
        # throw error if not possible
        form = forms.InterviewSchedulerForm()
        if request.method == 'POST':
            if form.validate_on_submit():
                # save info in session
                # check which button was pressed
                return redirect(url_for('.interviewscheduler', step=3))
    elif step is 3:
        form = forms.InterviewSchedulerForm()
    return render_template('interview_scheduler.html',
                           form=form,
                           **kwargs)


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
