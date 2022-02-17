from django.forms import Form, ModelForm, DateInput
from django.db import models
from .models import Booking

class BookingForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['start_date'].widget.attrs.update({'class': 'form-control', 'disabled': ''})
        self.fields['end_date'].widget.attrs.update({'class': 'form-control', 'disabled': ''})
        self.fields['guest_count'].widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = Booking
        exclude = ['code', 'price', 'room'] # These should not be set in the form