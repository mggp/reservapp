import bookings.models as m
from bookings.fields import ContactDetails
import datetime as dt

rt = m.RoomType(capacity = 1, name = 'Individual', daily_rate = 20.00)
rt.save()
for i in range(10):
    r = m.Room(name = '1{}'.format(i), room_type = rt)
    r.save()

rt = m.RoomType(capacity = 2, name = 'Doble', daily_rate = 30.00)
rt.save()
for i in range(5):
    r = m.Room(name = '2{}'.format(i), room_type = rt)
    r.save()

rt = m.RoomType(capacity = 3, name = 'Triple', daily_rate = 40.00)
rt.save()
for i in range(4):
    r = m.Room(name = '3{}'.format(i), room_type = rt)
    r.save()

rt = m.RoomType(capacity = 4, name = 'Cuádruple', daily_rate = 50.00)
rt.save()
for i in range(6):
    r = m.Room(name = '4{}'.format(i), room_type = rt)
    r.save()

r = m.Room.objects.all()[4]
b = m.Booking(
    start_date = dt.datetime(2022,2,18),
    end_date = dt.datetime(2022,2,20),
    code = 'MACBCKZ90F',
    price = r.room_type.daily_rate * 2,
    guest_count = 1,
    contact_info = ContactDetails(name='Publius Cornelius Scipio', email_address='cornelius@spqr.com', phone_number='+39 253 112'),
    room = r)

b.save()

r = m.Room.objects.all()[20]
b = m.Booking(
    start_date = dt.datetime(2022,2,20),
    end_date = dt.datetime(2022,2,22),
    code = '5UMZJJBO1B',
    price = r.room_type.daily_rate * 2,
    guest_count = 1,
    contact_info = ContactDetails(name='Hani Baal', email_address='hanibaal@spqr.com', phone_number='+216 111 111'),
    room = r)

b.save()