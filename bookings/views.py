from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.urls import reverse
from .models import Booking, Room, RoomType
from django.views.decorators.http import require_http_methods
from django.http import HttpResponseBadRequest, HttpResponseRedirect
from .forms import BookingForm
from .services import BookingService, RoomService, RoomTypeService

class BookingDetailsView(generic.DetailView):
    model = Booking

class BookingListView(generic.ListView):
    model = Booking

    def get_queryset(self):
        return Booking.objects.all()

    def get_context_data(self, **kwargs):
        ctxt = super().get_context_data(**kwargs)
        ctxt['nav_item_selected'] = 'Booking'
        return ctxt

class RoomListView(generic.ListView):
    model = Room

    def get_queryset(self):
        return Room.objects.all()

    def get_context_data(self, **kwargs):
        ctxt = super().get_context_data(**kwargs)
        ctxt['nav_item_selected'] = 'Room'
        return ctxt

class RoomTypeListView(generic.ListView):
    model = RoomType

    def get_queryset(self):
        params = self.request.GET
        
        capacity = params.get('guest_count', 0)
        try:
            capacity = int(capacity)
        except:
            capacity = 0

        return RoomType.objects.filter(capacity__gte = capacity)

    def get_context_data(self, **kwargs):
        ctxt = super().get_context_data(**kwargs)
        
        start_date = self.request.GET.get('start_date', None)
        end_date = self.request.GET.get('end_date', None)

        ctxt['nav_item_selected'] = 'RoomType'
        ctxt['guest_count'] = self.request.GET.get('guest_count', None)
        ctxt['start_date'] = start_date
        ctxt['end_date'] = end_date
        ctxt['test'] = {'attr':'funciona', 'attr2':'re funciona'}

        room_set = None
        if not start_date is None and not end_date is None:
            room_set = RoomService.GetAvailableRoomsForDateRange(start_date = start_date, end_date = end_date)
        
        ctxt['roomtype_list'] = RoomTypeService.ComputeRoomTypeBookingPriceForDateRange(ctxt['roomtype_list'].values(), start_date = start_date, end_date = end_date)
        ctxt['roomtype_list'] = RoomTypeService.ComputeRoomTypeAvailableCountFromAvailableRoomQuerySet(ctxt['roomtype_list'], room_set)

        return ctxt

@require_http_methods(["GET", "POST"])
def new_booking(request, room_type_id):
    if request.method == "GET":
        query_params = request.GET

        if not "start_date" in query_params or not "end_date" in query_params:
            return HttpResponseBadRequest("Se requiere fecha de check-in y check-out para crear reserva")

        room_type = get_object_or_404(RoomType, pk = room_type_id)
        
        guest_count = query_params.get('guest_count', default = room_type.capacity)
        start_date = query_params.get('start_date')
        end_date = query_params.get('end_date')

        try:
            price = BookingService.ComputePriceForDatesAndRoomType(start_date, end_date, room_type)
        except ValueError as e:
            return HttpResponseBadRequest("No se pudo calcular el precio para la reserva. "+ str(e))

        proto_booking = Booking(start_date = start_date, end_date = end_date, guest_count = guest_count, price = price)
        form = BookingForm(request.GET, instance = proto_booking)

        return render(request, "bookings/booking_form.html", {
            'nav_item_selected': None,
            'price': price,
            'maximum_room_capacity': room_type.capacity,
            'available_rooms': RoomService.GetAvailableRoomsOfRoomTypeForDateRange(start_date, end_date, room_type),
            'form': form, 
            'form_action': reverse('new_booking', args={room_type_id})})
    elif request.method == "POST":
        params = request.POST
        
        form = BookingForm(params)
        try:
            room_id = int(params.get('room_id'))
        except:
            return HttpResponseBadRequest()

        room_type = get_object_or_404(RoomType, pk = room_type_id)
        room = get_object_or_404(Room, pk = room_id)

        if room.room_type != room_type:
            return HttpResponseBadRequest()

        if (form.is_valid()):
            data = form.cleaned_data

            if data['guest_count'] > room_type.capacity:
                return HttpResponseBadRequest()
            if not RoomService.IsRoomAvailableForDates(room, data['start_date'], data['end_date']):
                return HttpResponseBadRequest()

            price = BookingService.ComputePriceForDatesAndRoomType(data['start_date'], data['end_date'], room_type)
            code = BookingService.GenerateCode()
            proto_booking = Booking(room=room, price=price, code=code, **data)
            proto_booking.save()

            return HttpResponseRedirect(reverse('booking_list'))
        else:
            return HttpResponseBadRequest(form.errors.as_json())