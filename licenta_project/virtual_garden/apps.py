from django.apps import AppConfig


class VirtualGardenConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'virtual_garden'

    def ready(self):
        import users.signals