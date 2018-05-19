from flask import Flask, render_template
from flask_sslify import SSLify

from app.login.admin_login_manager import login_manager

from app.admin.controllers import admin as admin_module
from app.user.controllers import user as user_module
from app.login.controllers import login as login_module


app = Flask(__name__, static_folder='static')
app.config.from_object('config')
sslify = SSLify(app)

login_manager.init_app(app)


@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')


@app.errorhandler(400)
def bad_request(error):
    return render_template('errors/400.html'), 400


@app.errorhandler(404)
def not_found(error):
    return render_template('errors/404.html'), 404


@app.errorhandler(500)
def internal_service(error):
    return render_template('errors/500.html'), 500


@app.errorhandler(503)
def service_unavailable(error):
    return render_template('errors/503.html'), 503


app.register_blueprint(login_module, url_prefix='/login')
app.register_blueprint(admin_module, url_prefix='/admin')
app.register_blueprint(user_module, url_prefix='/user')
