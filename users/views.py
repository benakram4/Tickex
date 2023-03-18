from django import forms
from django.http import HttpResponse
from django.shortcuts import redirect, render
from events.models import EventSeatType

from users.models import User, VenueOwnerProfile

from .forms import NewUserCreationForm

# enables list-based views in class-based views, 
 #this replaces querying the database in the function view below
from django.views.generic.edit import CreateView
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import DetailView, UpdateView
from django.views.generic.edit import DeleteView
# enables template-based views in class-based views
from django.views.generic import TemplateView

# does same as a login_required decorator just for class-based views
from django.contrib.auth.mixins import LoginRequiredMixin

###############################
#### Sign up & Login Views ####
###############################
class SignupView(CreateView):
    model = User
    form_class = NewUserCreationForm
    template_name = 'users/register.html'
    success_url = '/'

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # hide the admin type from the form
        form.fields['type'].choices = [
            (key, value) for key, value in form.fields['type'].choices if key != User.Types.ADMIN
        ]
        # make all the fields required
        for field in form.fields.values():
            field.required = True
        return form
            

class LogoutInterfaceView(LoginRequiredMixin, LogoutView):
    template_name = 'users/logout.html'
    login_url = 'login'


class LoginInterfaceView(LoginView):
    template_name = 'users/login.html'
    
    #if the user is already logged in, redirect to the home page
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('/')
        return super().get(request, *args, **kwargs)


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'users/dashboard.html'
    login_url = 'login'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        
        # get number of orders linked to the user in the ownerprofile
        context['num_orders'] = VenueOwnerProfile.objects.get(user=self.request.user).orders.count()
        
        context['quantity'] = 0
        context['balance'] = 0
        # check all  the quantity of the orders
        for order in VenueOwnerProfile.objects.get(user=self.request.user).orders.all():
            context['balance'] += EventSeatType.objects.get_seat_type_price(order.event_id, order.seat_type_id) * order.quantity
            context['quantity'] += order.quantity
        
        return context
    
#######################################
#### End og  Sign up & Login Views ####
#######################################

#######################################
####         User CRUD             ####
#######################################

class UserDeleteView(LoginRequiredMixin, DeleteView):
    model = User
    template_name = 'users/user_delete.html'
    success_url = '/'
    login_url = 'login'
    
    
class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'users/user_edit.html'
    form_class = NewUserCreationForm
    success_url = '/'
    login_url = 'login'
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # disable the type option and the username from the form
        form.fields['type'].widget.attrs['hidden '] = True
        form.fields['type'].label = ''
        # make all the fields required
        for field in form.fields.values():
            field.required = True
        return form
    
class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    context_object_name = 'user'
    template_name = 'users/user_detail.html'
    login_url = 'login'


#######################################
####       Rnd of User CRUD        ####
#######################################
    
