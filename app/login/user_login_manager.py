
from app.utils.mongo import Applicant, UnverifiedUserId


def valid_applicant(id):
    try:
        Applicant.objects().get(user_id=id)
        return True
    except (Applicant.DoesNotExist, Applicant.MultipleObjectsReturned):
        return False


def first_login(id):
    try:
        UnverifiedUserId.objects().get(user_id=id)
        return True
    except (UnverifiedUserId.DoesNotExist,
            UnverifiedUserId.MultipleObjectsReturned):
        return False
