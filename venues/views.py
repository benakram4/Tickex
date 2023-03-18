from django import forms
from django.shortcuts import render
from django.http import Http404, HttpResponseRedirect
# enables list-based views in class-based views,
from django.views.generic import CreateView, ListView, DetailView, UpdateView
                                            # this replaces querying the database in the function view below
from django.views.generic.edit import DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Venue
from .forms import VenueContactFormSet, VenueForm, VenueSeatTypeFormSet, VenueSeatTypeFormSetDeleteFalse

from .models import Venue
from .forms import VenueForm


# used this as a reference for the class-based view nested formset
# https://swapps.com/blog/working-with-nested-forms-with-django/


class VenueCreateView(LoginRequiredMixin, CreateView):
    model = Venue
    form_class = VenueForm
    template_name = 'venues/venue_form.html'
    success_url = '/venues/your-venues'
    login_url = 'login'
    
    # sets the owner_id to the current user
    def get_initial(self):
        initial = super().get_initial()
        initial['owner_id'] = self.request.user.id
        return initial

    # using the get_context_data method to pass the formset to the template
    def get_context_data(self, **kwargs):
        # we need to overwrite get_context_data
        # to make sure that our formset is rendered
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['contact'] = VenueContactFormSet(self.request.POST)
            context['seats'] = VenueSeatTypeFormSetDeleteFalse(self.request.POST)
        else:
            context['contact'] = VenueContactFormSet()
            context['seats'] = VenueSeatTypeFormSetDeleteFalse()
        return context
    
    # hide the owner_id field and label
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['owner_id'].widget = forms.HiddenInput()
        form.fields['owner_id'].label = ''
        return form
    

    def form_valid(self, form):
        # we need to overwrite form_valid
        # to make sure that our formset is saved
        context = self.get_context_data()
        contact = context['contact']
        seats = context['seats']
        self.object = form.save()
        if contact.is_valid() and seats.is_valid():
            contact.instance = self.object
            contact.save()
            seats.instance = self.object
            seats.save()
            return super().form_valid(form)
        else:
            return self.form_invalid(form)
            


class VenueListView(ListView):
    model = Venue
    template_name = 'venues/venues_list.html'
    context_object_name = 'venues'
    

class UserVenueListView(LoginRequiredMixin, ListView):
    model = Venue
    template_name = 'venues/user_venues.html'
    context_object_name = 'venues'
    login_url = 'login'
    
    def get_queryset(self):
        return self.request.user.venues.all()
    

class VenueDetailView(DetailView):
    model = Venue
    template_name = 'venues/venue_detail.html'
    context_object_name = 'venue'
    
    
class VenueDeleteView(LoginRequiredMixin, DeleteView):
    model = Venue
    template_name = 'venues/venue_delete.html'
    success_url = '/venues/your-venues'
    login_url = 'login'
    
    # only allow the owner of the venue to edit the venue
    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.owner_id_id != self.request.user.id:
            raise Http404
        return super().dispatch(request, *args, **kwargs)
    

class VenueUpdateView(LoginRequiredMixin, UpdateView):
    model = Venue    
    form_class = VenueForm
    template_name = 'venues/venue_edit.html'
    success_url = '/venues/your-venues'
    login_url = 'login'
    
    # only allow the owner of the venue to edit the venue
    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.owner_id_id != self.request.user.id:
            raise Http404
        return super().dispatch(request, *args, **kwargs)


    # sets the owner_id to the current user
    def get_initial(self):
        initial = super().get_initial()
        initial['owner_id'] = self.request.user.id
        return initial
    
    def get_context_data(self, **kwargs):
        # we need to overwrite get_context_data
        # to make sure that our formset is rendered.
        # the difference with CreateView is that
        # on this view we pass instance argument
        # to the formset because we already have
        # the instance created
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['contact'] = VenueContactFormSet(self.request.POST, instance=self.object)
            data['seats'] = VenueSeatTypeFormSet(self.request.POST, instance=self.object)
        else:
            data['contact'] = VenueContactFormSet(instance=self.object)
            data['seats'] = VenueSeatTypeFormSet(instance=self.object)
        return data
    
    # hide the owner_id field and label
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['owner_id'].widget = forms.HiddenInput()
        form.fields['owner_id'].label = ''
        return form
    
    def form_valid(self, form):
        # we need to overwrite form_valid
        # to make sure that our formset is saved
        context = self.get_context_data()
        contact = context['contact']
        seats = context['seats']
        self.object = form.save()
        if contact.is_valid() and seats.is_valid():
            contact.instance = self.object
            contact.save()
            seats.instance = self.object
            seats.save()
            return super().form_valid(form)
        else:
             return self.form_invalid(form)
           
    
    
    
    

    
    

