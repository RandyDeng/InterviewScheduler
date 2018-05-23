
from app.utils.mongo import Applicant, UnverifiedUser


def valid_applicant(id):
    try:
        Applicant.objects().get(user_id=id)
        return True
    except (Applicant.DoesNotExist, Applicant.MultipleObjectsReturned):
        return False


def first_login(id):
    try:
        UnverifiedUser.objects().get(user_id=id)
        return True
    except (UnverifiedUser.DoesNotExist,
            UnverifiedUser.MultipleObjectsReturned):
        return False
