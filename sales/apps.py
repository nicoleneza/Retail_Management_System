from django.apps import AppConfig

class SalesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'sales'
    
    # You can add more configuration here
    verbose_name = 'Sales Management'
    
    def ready(self):
        # This code runs when the app is ready
        # You can register signals here
        import sales.signals  # noqa
        # if you have any signals
