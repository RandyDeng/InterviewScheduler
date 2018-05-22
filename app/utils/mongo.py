import datetime
import json

from werkzeug import generate_password_hash

from mongoengine import (BinaryField, connect, DateTimeField, Document,
                         EmailField, EmbeddedDocument, EmbeddedDocumentField,
                         IntField, ListField, StringField)

from . import environment


# This grabs the environmental variable MONGODB link and
# establishes a connection to it. The database is
# available throughout the whole application after
# this initial connection is complete. Staging and Production
# use different MongoDB instances on Heroku.
uri = environment.variables['MONGODB_URI']
connect(host=uri)


# The following are 7 applicant states that determine
# what stage the applicant is in. Below is a description
# of what each stage means:
# REVIEW_PENDING - Application has been received and is under review
# REVIEW_REJECTION - Applicant has been rejected during the pre-screening phase
# INTERVIEW_PENDING - Application has been deemed okay and the applicant will
#                     now schedule an interview with the Elections Committee
# INTERVIEW_REJECTION - Applicant has been rejected during the interview phase
# CANDIDATE_PENDING - Applicant has passed the interview stage and will now be
#                     voted on by The Hive general body
# CANDIDATE_REJECTION - Applicant did not receive the highest number of votes
#                       and is thereby rejected
# ACCEPTANCE - Applicant has been accepted
# **IMPORTANT NOTE** CANDIDATE_PENDING and CANDIDATE_REJECTION only apply to
#                    Officer Positions
APPLICANT_STATUS = {
    0: 'REVIEW_PENDING',
    1: 'REVIEW_REJECTION',
    2: 'INTERVIEW_PENDING',
    3: 'INTERVIEW_REJECTION',
    4: 'CANDIDATE_PENDING',
    5: 'CANDIDATE_REJECTION',
    6: 'ACCEPTANCE'
}


class Applicant(Document):
    user_id = StringField(required=True)  # custom applicant identifier
    application_timestamp = DateTimeField(default=datetime.datetime.now)
    semester = StringField(default=environment.current_semester())
    status = StringField(default=APPLICANT_STATUS[0])

    #  Basic User Information
    first_name = StringField()
    last_name = StringField()
    email = EmailField()
    position = StringField()
    phone_number = StringField()
    year = StringField()
    expected_graduation_date = DateTimeField()
    on_campus = StringField()
    why_interested = StringField()
    comments = StringField()
    resume = BinaryField()  # file restricted to < 1MB and *.pdf only

    #  Officer Specific Information
    skills = StringField()


class TimeSlot(EmbeddedDocument):
    interviewee = StringField()
    start = DateTimeField()
    end = DateTimeField()
    length = IntField()  # length of time slot in minutes


class InterviewSchedule(Document):
    semester = StringField(default=environment.current_semester())
    timestamp = DateTimeField(default=datetime.datetime.now)
    timeslots = ListField(EmbeddedDocumentField(TimeSlot))


class UnverifiedUserId(Document):
    user_id = StringField()
    first_name = StringField()
    last_name = StringField()
    email = EmailField()
    position = StringField()


class Admins(Document):
    username = StringField()
    password = StringField()


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
