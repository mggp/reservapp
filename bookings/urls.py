from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.BookingListView.as_view(), name = "booking_list"),
    path('rooms/', views.RoomListView.as_view(), name = "room_list")
]