from django.db import models
import json

class ContactDetails:
    NAME = 'name'
    EMAIL_ADDRESS = 'email_address'
    PHONE_NUMBER = 'phone_number'
    
    CONTACT_FIELDS = (NAME, EMAIL_ADDRESS, PHONE_NUMBER)
    
    def __init__(self, args_dict):
        for key in self.CONTACT_FIELDS:
            try:
                self[key] = str(args_dict[key])
            except:
                # Does it ever raise an exception?
                print('Error processing field '+ key +' for ContactDetails')

class ContactDetailsField(models.TextField):
    name = models.CharField(max_length = 255, blank = True)
    email_address = models.EmailField(blank = True)    
    phone_number = models.CharField(max_length = 255, blank = True)

    def deserialize(obj_as_text) -> ContactDetails:
        obj_as_dict = json.loads(obj_as_text)

        return ContactDetails(obj_as_dict)     

    def to_python(self, value):
        if value is None:
            return value
        
        if isinstance(value, ContactDetails):
            return value

        return self.deserialize(value)

    def from_db_value(self, value, expression, connection):
        self.to_python(value)

    # TODO: Make serializer

class RoomType(models.Model):
    capacity = models.PositiveSmallIntegerField()
    daily_rate = models.DecimalField(decimal_places = 2, max_digits = 20)
    name = models.CharField(max_length = 255)

class Room(models.Model):
    room_type = models.ForeignKey(RoomType, on_delete = models.CASCADE)
    # It's a name and not a number in case there's a
    #  situation in which a name like '303bis' or sth is required  
    name = models.CharField(max_length = 255)    

class Booking(models.Model):
    start_date = models.DateField()
    end_date = models.DateField()
    code = models.CharField(
        max_length = 10, 
        unique = True, 
        primary_key = True)
    price = models.DecimalField(decimal_places = 2, max_digits = 20)
    guest_count = models.PositiveSmallIntegerField()
    # TODO: tidy/refactor contact details. Could also be a collection?
    contact_info = ContactDetailsField()
    room = models.ForeignKey(Room, on_delete = models.SET_NULL, null = True)


