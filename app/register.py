from framework.request_handler import SearchRequestHandler
from models.users import Users
from google.appengine.api import mail
from os import environ
import re


class RegisterUser(SearchRequestHandler):

    @classmethod
    def send_email(cls, to, user_id, confirmation_code):
        email_object = mail.EmailMessage(
            sender='noreply@todd-search.appspotmail.com',
            subject='Confirm your Recipe Search account',
            to=to
        )
        email_parameters = {
            'domain': 'http://localhost:10080:' if environ['SERVER_SOFTWARE'].startswith('Development') else 'http://todd-search.appspot.com',
            'user_id': user_id,
            'confirmation_code': confirmation_code
        }
        html_from_template = cls.jinja_environment.get_template('email/confirmation_email.html').render(email_parameters)

        email_object.html = html_from_template
        email_object.send()

    def post(self):
        name = self.request.get('name')
        email = self.request.get('email')
        password = self.request.get('password')
        status = 200
        json_response = {}
        if name and email and password:
            email_validation_pattern = "(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
            if re.match(email_validation_pattern, email):
                user = Users.add_new_user(name, email, password)
                if user['created']:
                    status = 200
                    html = self.jinja_environment.get_template('commons/register_modal_success.html').render()
                    json_response = {
                        'html': html
                    }
                    self.send_email(to=email, user_id=user['user_id'], confirmation_code=user['confirmation_code'])
                else:
                    status = 400
                    json_response = user
            else:
                status = 400
                json_response = {
                    'created': False,
                    'title': 'The email is not valid',
                    'message': 'Please enter a valid email address'
                }
        else:
            status = 400

            if not name:
                json_response.update({
                    'title': 'The Name field is required',
                    'message': 'Please fill in your name in order to continue'
                })
            if not email:
                json_response.update({
                    'title': 'You have not sent us an email!',
                    'message': 'Please send us a valid email address'
                })
            if not password:
                json_response.update({
                    'title': 'Please type in a password',
                    'message': 'Please fill in your password to continue'
                })

        self.json_response(status_code=status, **json_response)


class ConfirmUser(SearchRequestHandler):
    def get(self, user_id, confirmation_code):
        user = Users.get_by_id(int(user_id))

        if user:
            if user.confirmation_code == confirmation_code:
                user.confirmed_email = True
                user.put()

        self.redirect('/login')
