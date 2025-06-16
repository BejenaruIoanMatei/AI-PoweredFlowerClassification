from django.apps import AppConfig
from . import keras_utils

class BlogConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'blog'
    model_warmed_up = False
    
    def ready(self):
        if not BlogConfig.model_warmed_up:
            from . import keras_utils
            keras_utils.warm_up_model()
            BlogConfig.model_warmed_up = True