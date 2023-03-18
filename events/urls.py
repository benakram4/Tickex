from django.urls import path
from . import views

urlpatterns = [
    path('', views.EventListView.as_view(), name='event.list'),
    path('create/<int:pk>', views.EventCreateView.as_view(), name='event.create'),
    path('your-events', views.UserEventListView.as_view(), name='user.event.list'),
    path('<int:pk>', views.EventDetailView.as_view(), name='event.details'),
    path('<int:pk>/delete', views.EventDeleteView.as_view(), name='event.delete'),
    path('<int:pk>/update', views.EventUpdateView.as_view(), name='event.update'),
    
]