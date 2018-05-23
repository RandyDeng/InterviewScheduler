import os

from app.utils import environment

# Statement for enabling the development environment
DEBUG = False

# Define the application directory
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Application threads. A common general assumption is
# using 2 per available processor cores - to handle
# incoming requests using one and performing background
# operations using the other.
THREADS_PER_PAGE = 2

# Enable protection against *Cross-site Request Forgery (CSRF)*
CSRF_ENABLED = True

# Use a secure, unique and absolutely secret key for
# signing the data.
CSRF_SESSION_KEY = environment.ENV_VARIABLES['CSRF_SESSION_KEY']

# Secret key for signing cookies
SECRET_KEY = environment.ENV_VARIABLES['SECRET_KEY']

# Limit upload size to 3 MB before throwing errors
MAX_CONTENT_LENGTH = 3 * 1024 * 1024
