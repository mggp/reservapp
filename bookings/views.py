from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.urls import reverse
from .models import Booking, Room, RoomType
from django.views.decorators.http import require_http_methods
from django.http import HttpResponseBadRequest, HttpResponseRedirect
from .forms import BookingForm
from .services import BookingService

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

@require_http_methods(["GET", "POST"])
def new_booking(request, room_id):
    if request.method == "GET":
        query_params = request.GET

        if not "start_date" in query_params or not "end_date" in query_params:
            return HttpResponseBadRequest("Se requiere fecha de check-in y check-out para crear reserva")

        room = get_object_or_404(Room, pk = room_id)
        
        guest_count = query_params.get('guest_count', default = room.room_type.capacity)
        start_date = query_params.get('start_date')
        end_date = query_params.get('end_date')

        try:
            price = BookingService.ComputePriceForDatesAndRoom(start_date, end_date, room)
        except ValueError as e:
            return HttpResponseBadRequest("No se pudo calcular el precio para la reserva. "+ str(e))

        proto_booking = Booking(start_date = start_date, end_date = end_date, room = room, guest_count = guest_count, price = price)
        form = BookingForm(request.GET, instance = proto_booking)

        return render(request, "bookings/booking_form.html", {
            'nav_item_selected': None,
            'room': room,
            'price': price,
            'form': form, 
            'form_action': reverse('new_booking', args={room_id})})
    elif request.method == "POST":
        return HttpResponseRedirect(reverse('booking_list'))