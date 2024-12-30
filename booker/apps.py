from django.apps import AppConfig
from django.db.models.signals import post_migrate


class BookerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'booker'

    def ready(self):
        import booker.signals

        # from booker.models import ParkingSpace
        # from django.dispatch import receiver

        # This is needed, because on first launch, the field is empty, and you can't edit it, due to FKE
        # @receiver(post_migrate)
        # def create_default_parking_space(sender, **kwargs):
        #     if not ParkingSpace.objects.exists():
        #         ParkingSpace.objects.create(total_spaces=50)
