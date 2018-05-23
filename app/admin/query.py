import json
import urllib

from app.utils import environment, mongo


# default queries you can pass to the query page
current_semester = environment.current_semester()

current_all = urllib.parse.quote(json.dumps(
    {
        'title': 'All Applicants: ' + current_semester,
        'mongo_object': 'Applicant',
        'color': 'purple',
        'query': {
            'semester': current_semester
        }
    }))

current_accepted = urllib.parse.quote(json.dumps(
    {
        'title': 'Accepted Applicants: ' + current_semester,
        'mongo_object': 'Applicant',
        'color': 'green',
        'query': {
            'semester': current_semester,
            'status': mongo.APPLICANT_STATUS[6]
        }
    }))

current_remaining = urllib.parse.quote(json.dumps(
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

current_rejected = urllib.parse.quote(json.dumps(
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

all_unverified = urllib.parse.quote(json.dumps(
    {
        'title': 'Unverified Applicants',
        'mongo_object': 'UnverifiedUser',
        'color': 'purple',
        'query': {}

    }))

current_special = urllib.parse.quote(json.dumps(
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


def get_kwargs():
    return {
        'query_current_all': current_all,
        'query_current_remaining': current_remaining,
        'query_current_rejected': current_rejected,
        'query_current_accepted': current_accepted,
        'query_current_special': current_special,
        'query_all_unverified': all_unverified,
    }
