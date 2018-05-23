import smtplib
import jinja2

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from . import environment


FROM_ADDR = "The Hive: Interview Scheduler"


class Emailer():
    def __init__(self, to, subject, body):
        self._to = to
        self._subject = subject
        self._body = body

    def _connect(self):
        self._server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        self._server.ehlo()
        self._server.login(environment.ENV_VARIABLES['GMAIL_USERNAME'],
                           environment.ENV_VARIABLES['GMAIL_PASSWORD'])

    def _disconnect(self):
        self._server.quit()

    def send(self):
        msg = MIMEMultipart()
        msg['From'] = FROM_ADDR
        msg['To'] = self._to
        msg['Subject'] = self._subject
        msg.attach(MIMEText(self._body, 'html'))
        text = msg.as_string()
        self._connect()
        self._server.sendmail(FROM_ADDR, self._to, text)
        self._disconnect()


EMAIL_TEMPLATES = {
    'email_verification': jinja2.Template(open(
        'app/email_templates/email_verification.html').read()),
    'review_rejection': jinja2.Template(open(
        'app/email_templates/review_rejection.html').read()),
    'review_acceptance': jinja2.Template(open(
        'app/email_templates/review_acceptance.html').read()),
}


def send_email_template(to, template, context):
    rendered = EMAIL_TEMPLATES[template].render(context)
    mailer = Emailer(to, FROM_ADDR, rendered)
    mailer.send()
