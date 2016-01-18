from framework.request_handler import SearchRequestHandler
from lib.cloudstorage import cloudstorage_api
from google.appengine.api import blobstore
from google.appengine.api import images
from models.recipes import Recipes

class UserAccount(SearchRequestHandler):
    @SearchRequestHandler.login_required
    def get(self):
        user_id = self.check_user_logged_in.key.id()
        recipes = Recipes.get_all_recipes_by_user(user_id)

        tpl_values = {
            'recipes': recipes
        }

        self.render('account/home.html', **tpl_values)

class PostRecipe(SearchRequestHandler):
    @SearchRequestHandler.login_required
    def get(self):
        self.render('account/post_recipe.html')
    @SearchRequestHandler.login_required
    def post(self):
        user_key = self.check_user_logged_in.key
        title = self.request.get('title')
        cuisine = self.request.get('cuisine')
        difficulty = self.request.get('difficulty')
        cook_time = self.request.get('cook_time')
        prep_time = self.request.get('prep_time')
        ingredients = self.request.get('ingredients')
        directions = self.request.get('directions')
        photo = self.request.POST['image']

        saved_photo = self.save_image(photo, user_key)

        Recipes.add_new_recipe(
            title=title,
            cuisine=cuisine,
            difficulty=difficulty,
            prep_time=prep_time,
            cook_time=cook_time,
            ingredients=ingredients,
            directions=directions,
            user_key=user_key,
            photo_key=saved_photo['blobstore_key'],
            photo_url=saved_photo['serving_url']
        )

        self.redirect('/account')

    @classmethod
    def save_image(cls, photo, user_key):
        img_title = photo.filename
        img_content = photo.file.read()
        img_type = photo.type
        #todd-search-images is a google cloud bucket
        cloud_storage_path = '/gs/todd-search-images/%s/%s' % (user_key.id(), img_title)
        blobstore_key = blobstore.create_gs_key(cloud_storage_path)

        cloud_storage_file = cloudstorage_api.open(
            filename=cloud_storage_path[3:], mode='w', content_type=img_type
        )
        cloud_storage_file.write(img_content)
        cloud_storage_file.close()

        blobstore_key = blobstore.BlobKey(blobstore_key)
        serving_url = images.get_serving_url(blobstore_key)

        return {
            'serving_url': serving_url,
            'blobstore_key': blobstore_key
        }