from framework.request_handler import SearchRequestHandler
from models.recipes import Recipes

class RecipePage(SearchRequestHandler):
    def get(self, recipe_id):
        recipe = Recipes.get_by_id(int(recipe_id))

        template_values = {
            'recipe': recipe
        }

        self.render('recipe-page/recipe-page.html', **template_values)
