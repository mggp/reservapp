from django.forms import ModelForm, IntegerField
from .models import Booking

DEFAULT_INPUT_ATTRS = {'class': 'form-control text-end'}

class BookingForm(ModelForm):
    class Meta:
        model = Booking
        exclude = ['code', 'price', 'room'] # These should not be set in the form