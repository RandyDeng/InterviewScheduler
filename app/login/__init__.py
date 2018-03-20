from flask import Blueprint


login = Blueprint('login', __name__, url_prefix='/login',
                  template_folder='templates')
