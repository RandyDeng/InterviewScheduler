import datetime
import os


# Environment variables saved on Heroku
variables = {
  'BASE_URL': os.environ.get('BASE_URL'),
  'CSRF_SESSION_KEY': os.environ.get('CSRF_SESSION_KEY'),
  'GMAIL_PASSWORD': os.environ.get('GMAIL_PASSWORD'),
  'GMAIL_USERNAME': os.environ.get('GMAIL_USERNAME'),
  'MONGODB_URI': os.environ.get('MONGODB_URI'),
  'SECRET_KEY': os.environ.get('SECRET_KEY'),
}


# Dictionary of Available Positions
# Map: <key=abbreviation, value=position name>
# Not all positions will be available every semester
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


# Threshold values are hard-coded to determine Fall, Spring, Summer semester
fall_start = {'month': 8, 'day': 20}
spring_start = {'month': 1, 'day': 5}
summer_start = {'month': 5, 'day': 15}


# Determines the current semester
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


# Determines what the next 3 semesters are
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
