from django.apps import AppConfig
from django.db.models.signals import post_migrate
from .seed import *

class PinguinapiConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "pinguinAPI"

    def ready(self):
        from .seed import seed_muckie_products_post_migrate
        post_migrate.connect(seed_muckie_products_post_migrate, sender=self)

    
