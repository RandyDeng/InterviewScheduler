from flask import session


SESSION_METADATA = 'interview_scheduler_metadata'
SESSION_SCHEDULE = 'interview_scheduler_schedule'


def clean_metadata():
    session.pop(SESSION_METADATA)


def clean_schedule():
    session.pop(SESSION_SCHEDULE)


def clean_session():
    clean_metadata()
    clean_schedule()


def json_to_grid():
    pass


def generate_timeslots():
    pass
