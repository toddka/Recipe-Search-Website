from default.framework.request_handler import SearchRequestHandler
from google.appengine.api import taskqueue

class LoadURLs(SearchRequestHandler):
    def get(self):
        queue = taskqueue.Queue('parser')

        with open('modules/parser/src/food_com_small.txt', 'r') as list_urls:
            for url in list_urls:
                task = taskqueue.Task(url='/_parser/parse', params={'url': url.strip()})
                queue.add(task)
class Parse(SearchRequestHandler):
    def post(self):
        url = self.request.get('url')
