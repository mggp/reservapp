from django.contrib import admin

from bookings.models import Booking, Room, RoomType

admin.site.register(Booking)
admin.site.register(Room)
admin.site.register(RoomType)
