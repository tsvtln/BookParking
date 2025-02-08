from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, User
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as gl
from django.core.validators import RegexValidator
from django.contrib.auth.hashers import make_password


class AccountManager(BaseUserManager):
    """Custom manager for the Account model."""

    def create_user(self, nickname, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set.")
        if not nickname:
            raise ValueError("The Nickname field must be set.")
        email = self.normalize_email(email)
        extra_fields.setdefault("is_active", True)
        user = self.model(nickname=nickname, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, nickname, email, password=None, **extra_fields):
        """
        We can use this to further expand the admin logic and eventually create a proper panel with button on the
        frontend for admin users to manage the bookings and users.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(nickname, email, password, **extra_fields)


class Account(AbstractBaseUser, PermissionsMixin):
    nickname = models.CharField(
        max_length=30,
        unique=True,
        help_text="*Nicknames can contain only letters and digits.",
    )
    email = models.EmailField(
        max_length=100,
        unique=True,
        help_text="*Email address must be unique.",
    )
    first_name = models.CharField(max_length=30)
    second_name = models.CharField(max_length=30)
    phone_number = models.CharField(
        max_length=10,
        unique=True,
        null=True,
        blank=True,
        validators=[RegexValidator(r"^\d{10}$", "Enter a valid 10-digit phone number")],
    )
    profile_picture = models.ImageField(
        upload_to="profile_pictures/",
        null=True,
        blank=True,
        help_text="Upload a profile picture.",
    )
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = "nickname"
    REQUIRED_FIELDS = ["email"]

    objects = AccountManager()

    def save(self, *args, **kwargs):
        if not self.password.startswith("pbkdf2_"):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def clean(self):
        super().clean()
        if not self.nickname.isalnum() or len(self.nickname) < 3:
            raise ValidationError(gl("Your nickname is invalid!"))
        if not self.email.endswith("@pronetgaming.com"):
            raise ValidationError(gl("Only @pronetgaming.com emails are allowed!"))
        if Account.objects.filter(nickname__iexact=self.nickname).exists():
            raise ValidationError(gl("This nickname is already taken!"))

    def __str__(self):
        return f"{self.first_name} ({self.nickname}) {self.second_name}"


class ParkingSpace(models.Model):
    """
    A single record representing the universal number of parking spaces
    available each day (e.g., 42). We expect only 1 row/record in this table.
    Based on this a signal will be initiated to auto-populate for 365days the available spaces.
    """
    total_spaces = models.PositiveIntegerField(
        help_text='Total number of parking spaces available each day.'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if ParkingSpace.objects.exists() and not self.pk:
            # This is a fail-safe mechanism. Usually we shouldn't hit it, but if we somehow do, a manual edit in the DB
            #  will be required.
            raise ValidationError("You have to edit or remove the previous configuration of available spaces.")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Parking Space {self.total_spaces} total spaces left."


class ParkingAvailability(models.Model):
    date = models.DateField(
        unique=True,
        help_text='The date for which availability is being tracked.'
    )
    available_spaces = models.PositiveIntegerField(
        help_text="Number of spaces available for this day."
    )

    class Meta:
        ordering = ['date']

    def __str__(self):
        return f'{self.date}: {self.available_spaces}'

    def save(self, *args, **kwargs):
        """
        If creating a record, default available_spaces to ParkingSpace.total_spaces
        (the single record in the ParkingSpace table).
        """
        if not self.pk:  # only on create
            # grab the single ParkingSpace record (assuming only 1 record)
            space_record = ParkingSpace.objects.first()
            if not space_record:
                raise ValidationError("No ParkingSpace record found. Please create one first.")

            # use total_spaces from ParkingSpace as default
            self.available_spaces = space_record.total_spaces

        super().save(*args, **kwargs)


class Booking(models.Model):
    user = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        related_name='bookings',
        help_text="The user who booked this booking.",
    )

    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):

        if not hasattr(self, 'user') or not self.user or not self.user.pk:
            print("Skipping user-dependent validation in clean()")
            return

        # debug stuff
        if not self.user or not self.user.pk:
            raise ValidationError("User must be assigned before validation.")

        if Booking.objects.filter(user=self.user, date=self.date).exists():
            raise ValidationError("You have already booked a parking space for this date.")

        availability = ParkingAvailability.objects.filter(date=self.date).first()
        if not availability:
            raise ValidationError("No parking spaces available for this date!")

        if availability.available_spaces <= 0:
            raise ValidationError("No spaces available for this date!")

        if Booking.objects.filter(user=self.user, date=self.date).exists():
            # allow only 1 booking of a date per user
            raise ValidationError(gl('You have already booked a parking space for this date.'))

        availability = ParkingAvailability.objects.filter(date=self.date).first()
        if not availability:
            raise ValidationError(gl('No parking spaces available for this date!'))

        if availability.available_spaces <= 0:
            raise ValidationError(gl('No spaces available for this date!'))

    def save(self, *args, **kwargs):

        self.clean()

        # a lazy workaround if no value for parking spaces is preset
        space_record = ParkingSpace.objects.first()
        if not space_record:
            raise ValidationError("No ParkingSpace configured. Contact admin.")

        # availability check for the date
        availability, created = ParkingAvailability.objects.get_or_create(
            date=self.date,
            defaults={'available_spaces': space_record.total_spaces},
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
        return f'Booking by {self.user.nickname} for {self.date}'



