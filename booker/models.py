from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as gl


class Account(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='account',
        null=True,
        blank=True,
    )

    first_name = models.CharField(
        max_length=100,
        unique=False,
        help_text='Your first name',
    )

    second_name = models.CharField(
        max_length=100,
        unique=False,
        help_text='Your second name',
    )

    nickname = models.CharField(
        max_length=30,
        unique=True,
        help_text='*Nicknames can contain only letters and digits.'
    )

    email = models.EmailField(
        max_length=100,
        unique=True,
    )

    phone_number = models.CharField(
        max_length=15,
        unique=True,
        null=True,
        blank=True,
        help_text='Your phone number',
    )

    profile_picture = models.ImageField(
        upload_to='profile_pictures/',
        null=True,
        blank=True,
        help_text='Upload a profile picture',
    )

    def clean(self):
        super().clean()
        if not self.nickname.isalnum() or len(self.nickname) < 3:
            raise ValidationError(gl('Your nickname is invalid!'))
        if not self.email.endswith('@pronetgaming.com'):
            raise ValidationError(gl('Only @pronetgaming.com emails are allowed!'))
        if Account.objects.filter(nickname__iexact=self.nickname).exists():
            raise ValidationError(gl('This nickname is already taken!'))

    def __str__(self):
        return f"{self.first_name} ({self.nickname}) {self.second_name}"


class ParkingSpace(models.Model):
    total_spaces = models.PositiveIntegerField(
        help_text='Total number of parking spaces available each day.'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Parking Space {self.total_spaces} total spaces left."


class ParkingAvailability(models.Model):
    date = models.DateField(
        unique=True,
        help_text='The date for which availability is being tracked.'
    )

    available_spaces = models.PositiveIntegerField(
        help_text="Number of spaces available for parking spaces for this day."
    )

    class Meta:
        ordering = ['date']

    def __str__(self):
        return f'{self.date}: {self.available_spaces}'


class Booking(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='bookings',
        help_text="The user who booked this booking.",
    )

    date = models.DateField(
        help_text="The date for the parking is booked.",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        availability = ParkingAvailability.objects.filter(date=self.date).first()
        if not availability:
            raise ValidationError(gl('No parking spaces available for this date!'))

        if availability.available_spaces <= 0:
            raise ValidationError(gl('No spaces available for this date!'))

    def save(self, *args, **kwargs):

        # availability check for the date
        availability, created = ParkingAvailability.objects.get_or_create(
            date=self.date,
            defaults={'available_spaces': ParkingSpace.objects.first().total_spaces},
        )

        # check bf4 saving
        if availability.available_spaces <= 0:
            raise ValidationError(gl('No spaces available for this date!'))

        # deduct space
        availability.available_spaces -= 1
        availability.save()

        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # restore a spot availability
        availability = ParkingAvailability.objects.filter(date=self.date).first()
        if availability:
            availability.available_spaces += 1
            availability.save()

        super().delete(*args, **kwargs)

    def __str__(self):
        return f'Booking by {self.user.username} for {self.date}'

