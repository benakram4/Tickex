from django import forms
from .models import Event, EventSeatType

        
        
class EventSeatTypeForm(forms.ModelForm):
    class Meta:
        model = EventSeatType
        fields = "__all__"
        labels = {
            'available_seats' : 'Seats available (%)'
        }
         
EventSeatTypeFormSet = forms.inlineformset_factory(Event, EventSeatType, form=EventSeatTypeForm, extra=1, can_delete=True)
EventSeatTypeFormSetDeleteFalse = forms.inlineformset_factory(Event, EventSeatType, form=EventSeatTypeForm, extra=1, can_delete=False)


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = "__all__"
        labels = {
            'name': 'Event Name',
            'description': 'Description',
            'date': 'Date',
        }
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }