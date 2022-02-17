from django.db import models
from .fields import ContactDetailsModelField

# TODO: add field descriptions?
class RoomType(models.Model):
    capacity = models.PositiveSmallIntegerField()
    daily_rate = models.DecimalField(decimal_places = 2, max_digits = 20)
    name = models.CharField(max_length = 255)

    def __str__(self) -> str:
        return self.name

class Room(models.Model):
    room_type = models.ForeignKey(RoomType, on_delete = models.CASCADE)
    # It's a name and not a number in case there's a
    #  situation in which a name like '303bis' or sth is required  
    name = models.CharField(max_length = 255)

    def __str__(self) -> str:
        return " ".join((self.name, "("+str(self.room_type)+")"))

class Booking(models.Model):
    start_date = models.DateField()
    end_date = models.DateField()
    code = models.CharField(
        max_length = 10, 
        unique = True, 
        primary_key = True)
    price = models.DecimalField(decimal_places = 2, max_digits = 20)
    guest_count = models.PositiveSmallIntegerField()
    contact_info = ContactDetailsModelField()
    room = models.ForeignKey(Room, on_delete = models.SET_NULL, null = True)

    def __str__(self) -> str:
        return " ".join((
            self.code, 
            self.room.name, 
            "("+str(self.guest_count)+" PAX)", 
            "Check in:", str(self.start_date)))
