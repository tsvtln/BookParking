from django.apps import AppConfig


class BookerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'booker'

    def ready(self):
        # this I believe is needed for the signals to be ran, can't bother testing, so i just leave it here
        import booker.signals

