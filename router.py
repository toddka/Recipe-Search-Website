from webapp2 import WSGIApplication
from webapp2 import Route

app = WSGIApplication(
    routes=[
        Route('/', handler='app.home.Home'),
        Route('/register', handler='app.register.RegisterUser'),
        Route('/account/<user_id:[0-9]+>/confirm/<confirmation_code:[a-z0-9]{32}>', handler='app.register.ConfirmUser'),
        Route('/login', handler='app.login.LoginUser'),
        Route('/account', handler='app.account.UserAccount'),
        Route('/account/new-recipe', handler='app.account.PostRecipe'),
        Route('/search', handler='app.serp.SearchRecipes'),
        Route('/recipe/<recipe_id:[0-9]+>', handler='app.recipe.RecipePage'),
        ]
)