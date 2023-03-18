from django.urls import path
from . import views

urlpatterns = [
    path('signup', views.SignupView.as_view(), name='signup'),
    path('login', views.LoginInterfaceView.as_view(), name='login'),
    path('logout', views.LogoutInterfaceView.as_view(), name='logout'),
    path('dashboard', views.DashboardView.as_view(), name='dashboard'),
    path('user/<int:pk>', views.UserDetailView.as_view(), name='user.detail'),
    path('user/<int:pk>/edit', views.UserUpdateView.as_view(), name='user.edit'),
    path('user/<int:pk>/delete', views.UserDeleteView.as_view(), name='user.delete'),
]
