from django.forms import ModelForm
from .models import Booking

DEFAULT_INPUT_ATTRS = {'class': 'form-control text-end'}

class BookingForm(ModelForm):

    def __init__(self, *args, **kwargs):
        disabled_field_attrs = dict(DEFAULT_INPUT_ATTRS)
        disabled_field_attrs['disabled'] = ''

        super().__init__(*args, **kwargs)
        self.fields['start_date'].widget.attrs.update(disabled_field_attrs)
        self.fields['end_date'].widget.attrs.update(disabled_field_attrs)
        self.fields['guest_count'].widget.attrs.update(DEFAULT_INPUT_ATTRS)

    class Meta:
        model = Booking
        exclude = ['code', 'price', 'room'] # These should not be set in the form