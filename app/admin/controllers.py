from flask import abort, redirect, render_template
from flask_login import login_required

import json
import urllib

from app.utils import environment, mongo

from . import admin


@admin.route('/logout', methods=['GET'])
def logout():
    return redirect('login/admin')


@admin.route('/', methods=['GET'])
@admin.route('/dashboard', methods=['GET'])
@login_required
def dashboard():
    applications = mongo.Applicant.objects(
        semester=environment.current_semester()).count()
    total_applications = mongo.Applicant.objects.count()
    unverified_users = mongo.UnverifiedUserId.objects.count()
    return render_template('dashboard.html',
                           applications=applications,
                           total_applications=total_applications,
                           unverified_users=unverified_users)


@admin.route('/control_panel', methods=['GET'])
@login_required
def control_panel():
    return render_template('control_panel.html')


@admin.route('/applications', methods=['GET'])
@login_required
def applications():
    current_semester = environment.current_semester()
    query_current_all = urllib.parse.quote(json.dumps(
        {
            'title': 'All Applicants: ' + current_semester,
            'mongo_object': 'Applicant',
            'color': 'purple',
            'query': {
                'semester': current_semester
            }
        }))
    query_current_accepted = urllib.parse.quote(json.dumps(
        {
            'title': 'Accepted Applicants: ' + current_semester,
            'mongo_object': 'Applicant',
            'color': 'green',
            'query': {
                'semester': current_semester,
                'status': mongo.APPLICANT_STATUS[6]
            }
        }))
    query_current_remaining = urllib.parse.quote(json.dumps(
        {
            'title': 'Remaining Applicants: ' + current_semester,
            'mongo_object': 'Applicant',
            'color': 'orange',
            'query': {
                'semester': current_semester,
                'status': {
                    '$in': [
                        mongo.APPLICANT_STATUS[0],
                        mongo.APPLICANT_STATUS[2],
                        mongo.APPLICANT_STATUS[4],
                    ]
                }
            }
        }))
    query_current_rejected = urllib.parse.quote(json.dumps(
        {
            'title': 'Rejected Applicants: ' + current_semester,
            'mongo_object': 'Applicant',
            'color': 'red',
            'query': {
                'semester': current_semester,
                'status': {
                    '$in': [
                        mongo.APPLICANT_STATUS[1],
                        mongo.APPLICANT_STATUS[3],
                        mongo.APPLICANT_STATUS[5],
                    ]
                }
            }
        }))
    query_current_unverified = urllib.parse.quote(json.dumps(
        {
            'title': 'Unverified Users',
            'mongo_object': 'UnverifiedUserId',
            'color': 'purple',
            'query': {}

        }))
    query_current_special = urllib.parse.quote(json.dumps(
        {
            'title': 'Special Applicants: ' + current_semester,
            'mongo_object': 'Applicant',
            'color': 'orange',
            'query': {
                'semester': current_semester,
                'status': {
                    '$in': [
                        mongo.APPLICANT_STATUS[0],
                        mongo.APPLICANT_STATUS[2],
                        mongo.APPLICANT_STATUS[4],
                    ]
                }
            }
        }))
    return render_template('applications.html',
                           query_current_all=query_current_all,
                           query_current_remaining=query_current_remaining,
                           query_current_rejected=query_current_rejected,
                           query_current_accepted=query_current_accepted,
                           query_current_special=query_current_special,
                           query_current_unverified=query_current_unverified)


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
    elif mongo_object == 'UnverifiedUserId':
        unverified_users = mongo.UnverifiedUserId.objects(__raw__=query)
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
