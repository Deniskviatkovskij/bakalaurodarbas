from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('get_temperature/', views.get_temperature, name='get_temperature'),
    path('get_power/', views.get_power, name='get_power'),
    path('get_predicted_data/', views.get_predicted_data, name='get_predicted_data'),
    path('logout/', views.logout_view, name='logout'),
]
