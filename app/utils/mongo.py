import datetime
import json

from werkzeug import generate_password_hash

from mongoengine import (BinaryField, connect, DateTimeField, Document,
                         EmailField, StringField)

from . import environment


uri = environment.variables['MONGODB_URI']

# Connect to MongoEngine and MongoDB
connect(host=uri)

# Applicant status should not change
APPLICANT_STATUS = {
    0: 'REVIEW_PENDING',
    1: 'REVIEW_REJECTION',
    2: 'INTERVIEW_PENDING',
    3: 'INTERVIEW_REJECTION',
    4: 'CANDIDATE_PENDING',  # Only applicable to Officer Positions
    5: 'CANDIDATE_REJECTION',  # Only applicable to Officer Positions
    6: 'ACCEPTANCE'
}


class Applicant(Document):
    user_id = StringField(required=True)  # main applicant identifier
    application_timestamp = DateTimeField(default=datetime.datetime.now)
    semester = StringField(default=environment.current_semester())
    status = StringField(default=APPLICANT_STATUS[0])

    #  Basic User Information
    first_name = StringField(required=True)
    last_name = StringField(required=True)
    email = EmailField(required=True)
    position = StringField(required=True)
    phone_number = StringField()
    year = StringField()
    expected_graduation_date = DateTimeField()
    on_campus = StringField()

    #  Short Answer Information
    why_interested = StringField()
    comments = StringField()
    resume = BinaryField()

    #  Officer Specific Information
    skills = StringField()


class UnverifiedUserId(Document):
    user_id = StringField(required=True)
    first_name = StringField(required=True)
    last_name = StringField(required=True)
    email = EmailField(required=True)
    position = StringField(required=True)


class Admins(Document):
    username = StringField(required=True)
    password = StringField(required=True)


#  given Applicant, return UnverifiedUserID
def unverified_user_generator(applicant):
    user_id_json = {'first_name': applicant.first_name,
                    'last_name': applicant.last_name,
                    'email': applicant.email}
    return UnverifiedUserId(user_id=generate_password_hash(
                            json.dumps(user_id_json)),
                            first_name=applicant.first_name,
                            last_name=applicant.last_name,
                            email=applicant.email,
                            position=applicant.position)
