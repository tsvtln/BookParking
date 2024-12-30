from django.contrib import admin

from booker.models import ParkingSpace, ParkingAvailability, Booking


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
