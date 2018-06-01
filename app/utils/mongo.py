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
MONGODB_URI = environment.ENV_VARIABLES['MONGODB_URI']
connect(host=MONGODB_URI)


# The following are 7 applicant states that determine
# what stage the applicant is in. Below is a description
# of what each stage means:
# Application Pending - Application has been received and is under review
# Application Rejected - Applicant has been rejected during pre-screening
# Interview Pending - Application has been deemed okay and the applicant will
#                     now schedule an interview with the Elections Committee
# Interview Rejected - Applicant has been rejected during the interview phase
# Election Pending - Applicant has passed the interview stage and will now be
#                     voted on by The Hive general body
# Election Rejected - Applicant did not receive the highest number of votes
#                       and is thereby rejected
# Accepted - Applicant has been accepted
# **IMPORTANT NOTE** Election Pending and Election Rejected only apply to
#                    Officer Positions
APPLICANT_STATUS = {
    0: 'Application Pending',
    1: 'Application Rejected',
    2: 'Interview Pending',
    3: 'Interview Rejected',
    4: 'Election Pending',
    5: 'Election Rejected',
    6: 'Accepted'
}


# Given applicant data and officer decision, this will return
# the updated applicant status
def next_status(applicant, accepted):
    if applicant.status == APPLICANT_STATUS[0]:
        if accepted:
            return APPLICANT_STATUS[2]
        else:
            return APPLICANT_STATUS[1]
    if applicant.status == APPLICANT_STATUS[2]:
        if accepted and (applicant.position == environment.POSITIONS['PI']):
            return APPLICANT_STATUS[6]
        elif accepted:
            return APPLICANT_STATUS[4]
        else:
            return APPLICANT_STATUS[3]
    if applicant.status == APPLICANT_STATUS[4]:
        if accepted:
            return APPLICANT_STATUS[6]
        else:
            return APPLICANT_STATUS[5]
    return applicant.status


# The Applicant object contains all information regarding an Applicant.
# All Applicants will have data in each field unless the field is
# specific to a position. Some of the more basic data such as timestamps
# and semesters are autogenerated.
# NOTE: user_id must match the user_id emailed after the applicant fills out
#       the initial application
class Applicant(Document):
    user_id = StringField(required=True)
    application_timestamp = DateTimeField(default=datetime.datetime.now)
    semester = StringField(default=environment.current_semester())
    status = StringField(default=APPLICANT_STATUS[0])

    # Basic User Information
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

    # Officer Specific Information
    skills = StringField()


# Class that defines a time slot for scheduling interviews.
class TimeSlot(EmbeddedDocument):
    interviewee = StringField()
    start = DateTimeField()
    end = DateTimeField()
    length = IntField()  # length of time slot in minutes


# Document that holds a list of time slots for a given schedule during
# a semester. The timeslots ListField must be in ascending order
# for proper user viewing.
class InterviewSchedule(Document):
    semester = StringField(default=environment.current_semester())
    timestamp = DateTimeField(default=datetime.datetime.now)
    timeslots = ListField(EmbeddedDocumentField(TimeSlot))


# An UnverifiedUser is a user who only filled out the initial
# application but did not verify their email by completing the
# second form. UnverifiedUsers are deleted when necessary to keep
# the database clean.
class UnverifiedUser(Document):
    user_id = StringField()
    first_name = StringField()
    last_name = StringField()
    email = EmailField()
    position = StringField()


# This document holds the username and password for the admin login.
# There is only one account.
class Admins(Document):
    username = StringField()
    password = StringField()


# This document holds a string array of the positions available.
# This information is based off of the POSITIONS variable in environment.py.
# There is only one document containing this information.
class AvailablePositions(Document):
    available_positions = ListField(StringField())


# This generates an UnverifiedUser with a user_id based on the provided
# information. Generate password hash is used to generate the user_id.
def unverified_user_generator(**kwargs):
    kwargs['user_id'] = generate_password_hash(json.dumps(kwargs))
    return UnverifiedUser(**kwargs)
