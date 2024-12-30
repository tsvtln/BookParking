from datetime import timedelta, date
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import ParkingSpace, ParkingAvailability


@receiver(post_save, sender=ParkingSpace)
def populate_parking_availability(sender, instance, **kwargs):
    """
    Populate ParkingAvailability for the next 365 days based on ParkingSpace.
    """
    today = date.today()
    for i in range(365):
        day = today + timedelta(days=i)
        ParkingAvailability.objects.get_or_create(
            date=day,
            defaults={'available_spaces': instance.total_spaces},
        )


@receiver(post_save, sender=ParkingSpace)
def update_parking_availability(sender, instance, created, **kwargs):
    """
    Ensures ParkingAvailability records reflect the updated total_spaces value
    from ParkingSpace.
    """
    if not created:  # If this is an update to ParkingSpace
        # Update all existing ParkingAvailability records
        ParkingAvailability.objects.all().update(available_spaces=instance.total_spaces)
