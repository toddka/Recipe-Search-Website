from webapp2 import WSGIApplication
from webapp2 import Route

app = WSGIApplication(
    routes=[
        Route('/_parser/load', handler='modules.parser.src.food_website.LoadURLs'),
        Route('/_parser/parse', handler='modules.parser.src.food_website.Parse'),
    ]
)