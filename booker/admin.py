from django.contrib import admin
from booker.models import ParkingSpace, ParkingAvailability, Booking


# Admin Panel - Parking space fields (we can access the admin panel from http(s)://hostname-or-ip/admin)
# ID auto generated
# created_at is date of booking creation
# updated_at is date of last booking update
# total_spaces is the pre-configured total_space in the panel
# TODO: implement admin button on frontend to access the admin panel for admin/super users.
#  Alternatively, create a proper panel for admins, so they don't use the django panel.

@admin.register(ParkingSpace)
class ParkingSpaceAdmin(admin.ModelAdmin):
    list_display = ('id', 'total_spaces', 'created_at', 'updated_at')


@admin.register(ParkingAvailability)
class ParkingAvailabilityAdmin(admin.ModelAdmin):
    list_display = ('id', 'date', 'available_spaces')
    readonly_fields = ['available_spaces']
    ordering = ('date',)

    def get_readonly_fields(self, request, obj=None):
        """
        If the record is new (obj is None), we can allow editing.
        But if we truly never want it edited, always keep it read-only.
        """
        if not obj:
            # returning an empty list means user can set the field,
            # but we want to rely on model logic, so let's keep it read-only:
            return self.readonly_fields
        return self.readonly_fields


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'date', 'created_at')
    ordering = ('-created_at',)
