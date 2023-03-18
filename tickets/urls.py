from django.urls import path
from . import views

urlpatterns = [
     path('create/<int:event_id>/<int:seat_type_id>/', views.TicketCreateView.as_view(), name='create.ticket'),
     path('mytickets/', views.TicketView.as_view(), name='ticket.list'),
]
