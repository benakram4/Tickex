from django import forms
from .models import Ticket

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['event_id', 'seat_type_id', 'buyer_id', 'quantity']
        widgets = {
            'event_id': forms.HiddenInput(),
            'seat_type_id': forms.HiddenInput(),
            'buyer_id': forms.HiddenInput(),
        }
