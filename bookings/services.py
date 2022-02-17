from .models import Room, RoomType, Booking
from django.conf import settings
import datetime

class BookingService:
    
    def ComputePriceForDatesAndRoom(start_date, end_date, room):
        
        if not settings.BOOKING_MAX_DATE is None:
            last_possible_date = datetime.datetime.strptime(settings.BOOKING_MAX_DATE, '%Y-%m-%d')
        else:
            last_possible_date = datetime.datetime(datetime.now().year(), 12, 31)

        if isinstance(start_date, str):
            start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d')
        if isinstance(end_date, str):
            end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d')

        if start_date > end_date:
            raise ValueError('La fecha de salida tiene que ser posterior a la de entrada')
        if end_date > last_possible_date:
            raise ValueError(last_possible_date.strftime('La fecha de salida tiene que ser anterior a %Y-%m-%d'))
        
        stay = end_date - start_date
        return room.room_type.daily_rate * stay.days
