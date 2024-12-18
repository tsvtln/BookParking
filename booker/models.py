from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as gl

class Account(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='bookings',
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

    def clean(self):
        if not self.nickname.isalnum() or len(self.nickname) < 3:
            raise ValidationError(gl('Your nickname is invalid!'))

    def __str__(self):
        return self.nickname


