from django.apps import AppConfig
from . import keras_utils

class BlogConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'blog'
    
    def ready(self):
        from . import keras_utils
        dummy_prediction = keras_utils.warm_up_model()