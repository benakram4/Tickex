from django.views.generic.edit import CreateView
from django.views.generic.list import ListView

from venues.models import VenueSeatType
from .models import Ticket
from events.models import EventSeatType
from .forms import TicketForm
from events.models import Event
from django.contrib.auth.mixins import LoginRequiredMixin



class TicketCreateView(CreateView):
    model = Ticket
    form_class = TicketForm
    template_name = 'tickets/ticket_form.html'
    success_url = '/'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['event'] = Event.objects.get(id=self.kwargs['event_id'])
        context['venue_seat_type'] = VenueSeatType.objects.get(id=self.kwargs['seat_type_id'])
        
        # # get the total number of seats for the venue for the specific seat type
        # context['venue_total_seats'] = VenueSeatType.objects.get_total_seats_for_venue(context['event'].venue_id.id, context['venue_seat_type'].id)
        
        # event allocated seats for the specific seat type
        context['event_allocated_seats'] = EventSeatType.objects.get_total_seats_for_event(context['event'].id, context['venue_seat_type'].id)


        return context
    
    # initialize the form with the event_id and seat_type_id and buyer_id
    def get_initial(self):
        initial = super().get_initial()
        initial['event_id'] = self.kwargs['event_id']
        initial['seat_type_id'] = self.kwargs['seat_type_id']
        initial['buyer_id'] = self.request.user.id
        return initial

    # set the quantity max for 10 tickets for user of type "REGULAR"
    # for RESELLER, the min is 10 and max is 100
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        
        event = Event.objects.get(id=self.kwargs['event_id'])
        venue_seat_type = VenueSeatType.objects.get(id=self.kwargs['seat_type_id'])
        event_allocated_seats = EventSeatType.objects.get_total_seats_for_event(event.id, venue_seat_type.id)
        if self.request.user.type == 'REGULAR':
            form.fields['quantity'].widget.attrs['min'] = 1
            # if the event has less than 10 seats, set the max to the number of seats
            if event_allocated_seats < 10:
                form.fields['quantity'].widget.attrs['max'] = event_allocated_seats
            else:
                form.fields['quantity'].widget.attrs['max'] = 10
                
        elif self.request.user.type == 'RESELLER':
            # if the event has less than 100 seats, set the max to the number of seats
            if event_allocated_seats < 100:
                form.fields['quantity'].widget.attrs['max'] = event_allocated_seats
            else:
                form.fields['quantity'].widget.attrs['max'] = 100
            # if the min is less that 10, send an error message to the reseller 
            # that there are not enough tickers for reselling   
            if event_allocated_seats < 10:
                form.fields['quantity'].widget.attrs['min'] = 0
                form.fields['quantity'].widget.attrs['max'] = 0
                form.fields['quantity'].widget.attrs['disabled'] = True
            else:
                form.fields['quantity'].widget.attrs['min'] = 10

        return form

class TicketView(LoginRequiredMixin,ListView):
    model = Ticket
    context_object_name = 'tickets'
    template_name = "tickets/my_tickets.html"
    login_url = 'login'
    
