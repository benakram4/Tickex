import math
from django import forms
from django.http import Http404
from django.shortcuts import render
from django.views.generic import CreateView, ListView, DetailView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin

from venues.models import Venue, VenueSeatType

from .models import Event, EventSeatType
from .forms import EventForm, EventSeatTypeFormSet, EventSeatTypeFormSetDeleteFalse

class EventCreateView(LoginRequiredMixin, CreateView):
    model = Event
    form_class = EventForm
    template_name = 'events/event_form.html'
    success_url = '/'
    login_url = 'login'
    
    # only the venue owner can create an event for their venue
    def dispatch(self, request, *args, **kwargs):
        venue_pk = self.kwargs['pk']
        venue = Venue.objects.get(pk=venue_pk)
        if venue.owner_id_id != self.request.user.id:
            raise Http404
        return super().dispatch(request, *args, **kwargs)
    
    
    def get_initial(self):
        venue_pk = self.kwargs['pk']
        initial = super().get_initial()
        initial['venue_id'] = venue_pk
        return initial

    
    def get_context_data(self, **kwargs):
        # we need to overwrite get_context_data
        # to make sure that our formset is rendered
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['seat'] = EventSeatTypeFormSetDeleteFalse(self.request.POST)
        else:
            context['seat'] = EventSeatTypeFormSetDeleteFalse()
        # get all the seat types for the venue
        venue_pk = self.kwargs['pk']
        venue = Venue.objects.get(pk=venue_pk)
        # show only the seat types that are available for the venue
        context['seat'].forms[0].fields['venue_seat_type_id'].queryset = venue.seat_types.all()
        
        # limit seat selection 100 as its in percentage
        context['seat'].forms[0].fields['available_seats'].widget.attrs['max'] = 100
        context['seat'].forms[0].fields['available_seats'].widget.attrs['min'] = 0
        return context
    
    #hide the venue_id field and label
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['venue_id'].widget = forms.HiddenInput()
        form.fields['venue_id'].label = ''
        return form
    
    def form_valid(self, form):
        context = self.get_context_data()
        seat = context['seat']
        self.object = form.save()
        if seat.is_valid():
            seat.instance = self.object
            seat.save()
            return super().form_valid(form)
        else:
             return self.form_invalid(form)

class EventListView(ListView):
    model = Event
    context_object_name = "events"
    template_name = "events/events_list.html"
    
class UserEventListView(LoginRequiredMixin, ListView):
    model = Event
    template_name = "events/user_events.html"
    context_object_name = "events"
    login_url = 'login'
    
    # only show the events for the venues that the user owns
    def get_queryset(self):
        venueEvents = []
        for venue in self.request.user.venues.all():
            venueEvents += venue.events.all()
        return venueEvents
    

class EventDetailView(DetailView):
    model = Event
    context_object_name = "event"
    template_name = "events/event_detail.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Names
        context['seat_types'] = EventSeatType.objects.filter(event_id=self.object.id)
        context['seat_types'] = [seat_type.venue_seat_type_id for seat_type in context['seat_types']]
        context['seat_types'] = [seat_type.name for seat_type in context['seat_types']]

        # Prices
        context['seat_types_prices'] = EventSeatType.objects.filter(event_id=self.object.id)
        context['seat_types_prices'] = [seat_type.price for seat_type in context['seat_types_prices']]

        # get the seat types id
        context['seat_types_id'] = EventSeatType.objects.filter(event_id=self.object.id)
        context['seat_types_id'] = [seat_type.venue_seat_type_id for seat_type in context['seat_types_id']]
        context['seat_types_id'] = [seat_type.id for seat_type in context['seat_types_id']]
        
        # Total Seats for each seat type in the venue
        context['venue_total_seat_type'] = EventSeatType.objects.filter(event_id=self.object.id)
        context['venue_total_seat_type'] = [seat_type.venue_seat_type_id for seat_type in context['venue_total_seat_type']]
        context['venue_total_seat_type'] = [seat_type.total_seats for seat_type in context['venue_total_seat_type']]
        
        # percentage os Seats allocated for each seat type in the venue for the event
        context['seat_types_allocated_seats'] = EventSeatType.objects.filter(event_id=self.object.id)
        context['seat_types_allocated_seats'] = [seat_type.available_seats for seat_type in context['seat_types_allocated_seats']]
        
        # get the total seats for each seat type in the venue
        context['event_total_seat_type'] = [int(total_seats * allocated_seats / 100) for total_seats, allocated_seats in zip(context['venue_total_seat_type'], context['seat_types_allocated_seats'])]

        # all the data together
        context['seat_types_prices'] = [(event_seats, seat_type, str(price), str(seat_type_id)) 
                                        for event_seats, seat_type, price, seat_type_id in 
                                        zip(context['event_total_seat_type'],
                                          context['seat_types'], context['seat_types_prices'], context['seat_types_id'])]
        
        # DEBUG PRINTS
        # print('\n\n\n\n\n')
        # print (context['seat_types_prices'])
        # print('\n\n\n\n\n')
        return context
    
    
class EventDeleteView(LoginRequiredMixin, DeleteView):
    model = Event
    context_object_name = "event"
    template_name = "events/event_delete.html"
    success_url = '/'
    login_url = 'login'
    
    
    # only allow the owner of the venue to delete the event
    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.venue_id.owner_id_id != self.request.user.id:
            raise Http404
        return super().dispatch(request, *args, **kwargs)
    
class EventUpdateView(LoginRequiredMixin, UpdateView):
    model = Event
    form_class = EventForm
    template_name = 'events/event_edit.html'
    success_url = '/events/your-events'
    login_url = 'login'
    
    # only the venue owner can create an event for their venue
    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.venue_id.owner_id_id != self.request.user.id:
            raise Http404
        return super().dispatch(request, *args, **kwargs)
    
    # set the initial value for the venue_id field
    def get_initial(self):
        initial = super().get_initial()
        initial['venue_id'] = self.object.venue_id.id
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['seat'] = EventSeatTypeFormSet(self.request.POST, instance=self.get_object())
        else:
            context['seat'] = EventSeatTypeFormSet(instance=self.get_object())
  
        # get all the seat types for the venue
        venue_pk = self.object.venue_id.id
        venue = Venue.objects.get(pk=venue_pk)

        # show only the seat types that are available for the venue for all nest forms
        for form in context['seat'].forms:
            form.fields['venue_seat_type_id'].queryset = venue.seat_types.all()

        # get all seat types for the event
        event_pk = self.object.id
        event = Event.objects.get(pk=event_pk)
        event_seat_types = EventSeatType.objects.filter(event_id=event_pk)
        event_seat_types = event_seat_types.values_list('venue_seat_type_id', flat=True)
        
        #make selected seat types read only
        for form in context['seat'].forms:
            # limit seat selection 100 as its in percentage
            form.fields['available_seats'].widget.attrs['max'] = 100 # max in 100%
            form.fields['available_seats'].widget.attrs['min'] = 1
            if form.instance.venue_seat_type_id_id in event_seat_types:
                # show the seat type as the one selected
                form.fields['venue_seat_type_id'].queryset = venue.seat_types.filter(id__in=event_seat_types)
                # make the field read only
                form.fields['venue_seat_type_id'].widget.attrs['readonly'] = True
                #disable the field
                form.fields['venue_seat_type_id'].disabled = True
            else:
                #remove already selected seat types from the queryset, only if the field is not read only
                form.fields['venue_seat_type_id'].queryset = venue.seat_types.exclude(id__in=event_seat_types)
    
        # TODO Delete this code later, still need it for reference
        # # limit the number of seats for each seat type in venue
        # for form in context['seat'].forms:
        #     if  form.instance.id is not None:
        #         # get the venue id and the seat type id
        #         venue_id = form.instance.venue_seat_type_id_id
        #         venue_seat_type = VenueSeatType.objects.get(pk=venue_id)
        #         venue_seat_type_max = venue_seat_type.total_seats
          
        return context
    
    #hide the venue_id field and label
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['venue_id'].widget = forms.HiddenInput()
        form.fields['venue_id'].label = ''
        return form
    
    def form_valid(self, form):
        context = self.get_context_data()
        seat = context['seat']
        self.object = form.save()
        if seat.is_valid():
            seat.instance = self.object
            seat.save()
            return super().form_valid(form)
        else:
             return self.form_invalid(form)

    
