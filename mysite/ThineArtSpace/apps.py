from django.apps import AppConfig


class ThineartspaceConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ThineArtSpace'

    def ready(self):
        from .signals import create_profile, save_profile
