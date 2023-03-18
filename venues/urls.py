from django.urls import path
from . import views

urlpatterns = [
    path('', views.VenueListView.as_view(), name='venue.list'),
    path('create', views.VenueCreateView.as_view(), name='venue.create'),
    path('your-venues', views.UserVenueListView.as_view(), name='user.venue.list'),
    path('<int:pk>', views.VenueDetailView.as_view(), name='venue.detail'),
    path('<int:pk>/delete', views.VenueDeleteView.as_view(), name='venue.delete'),
    path('<int:pk>/update', views.VenueUpdateView.as_view(), name='venue.update'),
]