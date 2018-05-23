import datetime
import os


# Environmental variables are stored inside a .env file for
# testing locally and on Heroku for staging and production.
# These variables contain extremely sensitive information regarding
# the project and should not be disclosed to anyone except
# the developers working on this project.
variables = {
  'BASE_URL': os.environ.get('BASE_URL'),
  'CSRF_SESSION_KEY': os.environ.get('CSRF_SESSION_KEY'),
  'GMAIL_PASSWORD': os.environ.get('GMAIL_PASSWORD'),
  'GMAIL_USERNAME': os.environ.get('GMAIL_USERNAME'),
  'MONGODB_URI': os.environ.get('MONGODB_URI'),
  'SECRET_KEY': os.environ.get('SECRET_KEY'),
}


# The following is a dictionary of all the available
# positions in The Hive. Each position is matched with its
# abbreviated version. Not all positions will be available
# at all times and some may not go through the Interview Scheduler
# process.
# Currently, only PI and the core officer positions are supported.
positions = {
    'MPI': 'Master Peer Instructor',
    'PI': 'Peer Instructor',
    'President': 'President',
    'VP': 'Vice President',
    'DoF': 'Director of Finances',
    'DoO': 'Director of Operations',
    'DoC': 'Director of Communications',
    'DoN': 'Director of Networks',
    'ADoF': 'Assistant Director of Finances',
    'ADoO': 'Assistant Director of Operations',
    'ADoC': 'Assistant Director of Communications',
    'ADoN': 'Assistant Director of Networks'
}


# These variables determine the start and end of each school semester.
# The starting dates are put slightly before the first day of class
# since most of The Hive hiring happens at the beginning of the semester
# rather than at the end.
fall_start = {'month': 8, 'day': 15}
spring_start = {'month': 1, 'day': 1}
summer_start = {'month': 5, 'day': 10}


# Determines the current semester.
# The semester start and end dates are hardcoded.
def current_semester():
    now = datetime.date.today()
    fall_begin = datetime.date(year=now.year,
                               month=fall_start['month'],
                               day=fall_start['day'])
    spring_begin = datetime.date(year=now.year,
                                 month=spring_start['month'],
                                 day=spring_start['day'])
    spring_next = spring_begin.replace(year=now.year + 1)
    summer_begin = datetime.date(year=now.year,
                                 month=summer_start['month'],
                                 day=summer_start['day'])

    if now > fall_begin and now < spring_next:
        return ("Fall " + str(now.year))
    if now > spring_begin and now < summer_begin:
        return ("Spring " + str(now.year))
    if now > summer_begin and now < fall_begin:
        return ("Summer " + str(now.year))
    return "NA"


# Determines the next 3 semesters.
# This is mainly used in the Applicant form to determine which
# semesters an applicant will be on campus.
def next_semesters():
    current = current_semester().split()
    next_year = str(int(current[1]) + 1)
    if "Fall" in current:
        future = ["Spring " + next_year,
                  "Summer " + next_year,
                  "Fall " + next_year]
    elif "Spring" in current:
        future = ["Summer " + current[1],
                  "Fall " + current[1],
                  "Spring " + next_year]
    elif "Summer" in current:
        future = ["Fall " + current[1],
                  "Spring " + next_year,
                  "Summer " + next_year]
    else:
        future = None
    return future
