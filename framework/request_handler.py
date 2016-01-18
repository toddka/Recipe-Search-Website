from webapp2 import RequestHandler
from webapp2 import cached_property
import os
import jinja2

class SearchRequestHandler(RequestHandler):
    template_directory = os.path.join(
        os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)),
        'templates')
    jinja_environment = jinja2.Environment(
        loader=jinja2.FileSystemLoader(template_directory)
    )

    def render(self, template, **kwargs):
        jinja_template = self.jinja_environment.get_template(template)
        html_from_template = jinja_template.render(kwargs)

        self.response.out.write(html_from_template)

    def json_response(self, status_code=200, **kwargs):
        from json import dumps

        self.response.status = status_code
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(dumps(kwargs))
    def read_cookie(self, name):
        from framework.cookie_handler import check_cookie

        cookie_value = self.request.cookies.get(name)
        return check_cookie(cookie_value)
    def send_cookie(self, name, value):
        from framework.cookie_handler import sign_cookie

        signed_cookie_value = sign_cookie(value)
        self.response.headers.add_header('Set-Cookie', '%s=%s; Path=/' % (name, signed_cookie_value))
    @cached_property
    def check_user_logged_in(self):
        if self.request.cookies.get('User'):
            user_id = self.read_cookie('User')
            if user_id:
                from models.users import Users
                return Users.get_by_id(int(user_id))
            else:
                return None
        return None
    @staticmethod
    def login_required(handler):
        def check_login(self, *args, **kwargs):
            if self.check_user_logged_in:
                return handler(self, *args, **kwargs)
            else:
                return self.redirect('/login')
        return check_login

