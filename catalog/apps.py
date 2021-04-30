from django.apps import AppConfig

# Pointer needed for ../locallibrary/settings.py to find the location of our catalog app.
class CatalogConfig(AppConfig):
    name = 'catalog'
