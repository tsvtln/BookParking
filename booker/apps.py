from django.apps import AppConfig


class BookerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'booker'

    # this I believe is needed for the signals to be ran, can't bother testing, so just leave it here
    def ready(self):
        import booker.signals

