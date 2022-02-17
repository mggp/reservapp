from .models import Room, RoomType, Booking
from django.conf import settings
from django.db.models import Q
import datetime

class BookingService:
    
    def ComputePriceForDatesAndRoomType(start_date, end_date, room_type):
        
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
        return room_type.daily_rate * stay.days

class RoomService:

    def GetAvailableRoomsForDateRange(start_date, end_date, *args):
        # Bookings that start before query range and end after range start
        checkin_unavailable_query = {'booking__start_date__lte': start_date, 'booking__end_date__gt': start_date}
        # Bookings that start after query range and before range end
        checkout_unavailable_query = {'booking__start_date__gte': start_date, 'booking__start_date__lt': end_date}
        
        available_rooms_query = ~Q(**checkin_unavailable_query) & ~Q(**checkout_unavailable_query)

        extra_queries = Q()
        for a in args:
            if isinstance(a, Q):
                extra_queries = a & extra_queries
        
        try:
            datetime.datetime.strptime(start_date,"%Y-%m-%d")
            datetime.datetime.strptime(end_date,"%Y-%m-%d")    

            return Room.objects.filter(available_rooms_query & extra_queries)
        except:
            return Room.objects.filter(extra_queries)

    def GetAvailableRoomsOfRoomTypeForDateRange(start_date, end_date, room_type):
        room_type_query = {'room_type__id': room_type.id}
        
        return RoomService.GetAvailableRoomsForDateRange(start_date, end_date, Q(**room_type_query))


    def GetAvailableRoomsForDateRangeAndMinimumRoomTypeCapacity(start_date, end_date, capacity=0):
        capacity_query = {'room_type__capacity__gte': capacity}
        
        return RoomService.GetAvailableRoomsForDateRange(start_date, end_date, Q(**capacity_query))

        

class RoomTypeService:

    def ComputeRoomTypeBookingPriceForDateRange(room_types, start_date, end_date):
        try:
            s = datetime.datetime.strptime(start_date,"%Y-%m-%d")
            e = datetime.datetime.strptime(end_date,"%Y-%m-%d")    

            if (e < s):
                raise ValueError()

            day_count = (e - s).days
        except:
            day_count = 0

        for rt in room_types:
            rt['booking_price'] = rt['daily_rate'] * day_count

        return room_types

    def ComputeRoomTypeAvailableCountFromAvailableRoomQuerySet(room_types, rooms = None):
        if rooms is None:
            rooms = Room.objects.all()
        
        for rt in room_types:
            rt['available_count'] = rooms.filter(room_type__id = rt['id']).count()

        return room_types