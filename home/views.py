from django.shortcuts import render

#Added imports for class-based views
from django.views.generic import TemplateView # enables template-based views in class-based views

from events.models import Event
#query the first 3 events
class HomeView(TemplateView):
    template_name = 'home/home_page.html'
    def get_context_data(self, **kwargs): 
        
        # the 5 most recent events
        events = Event.objects.all().order_by('-date')[:5]
        
        context = super().get_context_data(**kwargs)
        context['events'] = events
                
        return context
