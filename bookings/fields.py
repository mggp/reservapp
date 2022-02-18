from multiprocessing.sharedctypes import Value
from django.forms import MultiWidget, TextInput, EmailInput, MultiValueField, CharField, EmailField
from django.db import models
import json

class ContactDetails(dict):
    NAME = 'name'
    EMAIL_ADDRESS = 'email_address'
    PHONE_NUMBER = 'phone_number'
    
    CONTACT_FIELDS = (NAME, EMAIL_ADDRESS, PHONE_NUMBER)
    
    def __init__(self, **kwargs):
        for key in self.CONTACT_FIELDS:
            try:
                self[key] = str(kwargs[key])
            except:
                self[key] = None
    
class ContactDetailsWidget(MultiWidget):

    def __init__(self, attrs = None, **kwargs):
        widgets = [
            TextInput(),
            EmailInput(),
            TextInput(),
        ]
        
        super().__init__(widgets = widgets, **kwargs)

    def get_context(self, name, value, *attrs, **kwargs):
        proto_context = super().get_context(name, value, *attrs, **kwargs)
        
        LABELS = ('Nombre', 'Correo electrónico', 'Número de teléfono')
        for count, widget in enumerate(proto_context['widget']['subwidgets']):
            widget['template_name'] = 'bookings/widgets/sub_contact_details.html'
            if widget['value'] is None:
                widget['value'] = ''
            widget['label'] = LABELS[count]
            widget['input_name'] = ContactDetails.CONTACT_FIELDS[count]
        
        return proto_context
    
    def decompress(self, value):
        if not value:
            return [None, None, None]
        
        json_val = json.loads(value)

        return [
            json_val['name'],
            json_val['email_address'],
            json_val['phone_number']
        ]


class ContactDetailsField(MultiValueField):
    def __init__(self, **kwargs):
        fields = (
            CharField(required = True, label = 'Name'),
            EmailField(required = True, label = 'Email address'),
            CharField(required = True, label = 'Phone number'),            
        )
        kwargs['widget'] = ContactDetailsWidget
        kwargs['fields'] = fields
        kwargs.pop('max_length', None)
        super().__init__(require_all_fields = True, **kwargs)

    def compress(self, data_list):
        return json.dumps({'name': data_list[0], 'email_address': data_list[1], 'phone_number': data_list[2]})

class ContactDetailsModelField(models.TextField):
    def formfield(self, **kwargs):
        defaults = {'form_class': ContactDetailsField}
        defaults.update(kwargs)
        return super().formfield(**defaults)

    def to_python(self, value):
        if value is None:
            return value
        
        if isinstance(value, ContactDetails):
            return value

        return ContactDetails(**json.loads(value))

    def get_prep_value(self, value):
        return json.dumps(value)

    def value_to_string(self, obj) -> str:
        return json.dumps(obj)
    