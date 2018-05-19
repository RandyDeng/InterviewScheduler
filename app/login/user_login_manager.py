from flask import flash

from app.utils.mongo import Applicant, UnverifiedUserId


def valid_applicant(id, flashing):
    try:
        Applicant.objects().get(user_id=id)
        return True
    except (Applicant.DoesNotExist, Applicant.MultipleObjectsReturned):
        if flashing:
            flash("You are not authorized to access this page",
                  'alert alert-danger')
        return False


def first_login(id, flashing):
    try:
        UnverifiedUserId.objects().get(user_id=id)
        return True
    except (UnverifiedUserId.DoesNotExist,
            UnverifiedUserId.MultipleObjectsReturned):
        if flashing:
            flash("You are not authorized to access this page",
                  'alert alert-danger')
        return False
