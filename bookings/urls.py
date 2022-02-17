from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.BookingListView.as_view(), name = "booking_list"),
    path('rooms/', views.RoomListView.as_view(), name = "room_list"),
    path('room_types/', views.RoomTypeListView.as_view(), name = "room_type_list"),
    path('room/<int:room_type_id>/bookings/new', views.new_booking, name = "new_booking"),
]