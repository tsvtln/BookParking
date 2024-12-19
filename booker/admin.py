from django.contrib import admin
from .models import ParkingSpace, ParkingAvailability, Booking


@admin.register(ParkingSpace)
class ParkingSpaceAdmin(admin.ModelAdmin):
    list_display = ('total_spaces', 'created_at', 'updated_at')


@admin.register(ParkingAvailability)
class ParkingAvailabilityAdmin(admin.ModelAdmin):
    list_display = ('date', 'available_spaces')
    ordering = ('date',)


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'created_at')
    ordering = ('-created_at',)
