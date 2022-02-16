from django.shortcuts import render
from django.views import generic
from .models import Booking, Room, RoomType

def booking_details(request, booking_code):
    pass

class BookingDetailsView(generic.DetailView):
    model = Booking

def booking_form(request):
    pass

def booking_list(request):
    pass

class BookingListView(generic.ListView):
    model = Booking

    def get_queryset(self):
        return Booking.objects.all()

    def get_context_data(self, **kwargs):
        ctxt = super().get_context_data(**kwargs)
        ctxt['nav_item_selected'] = 'Booking'
        return ctxt

def search_for_available_rooms(request): # TODO: This name is not quite right, change it
    pass

class RoomListView(generic.ListView):
    model = Room

    def get_queryset(self):
        return Room.objects.all()

    def get_context_data(self, **kwargs):
        ctxt = super().get_context_data(**kwargs)
        ctxt['nav_item_selected'] = 'Room'
        return ctxt