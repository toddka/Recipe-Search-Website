from framework.request_handler import SearchRequestHandler

class Home(SearchRequestHandler):
    def get(self):
        self.render('home/home.html')