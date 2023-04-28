from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('get_temperature/', views.get_temperature, name='get_temperature'),
    path('get_voltage/', views.get_voltage, name='get_voltage'),
    path('get_predicted_data/', views.get_predicted_data, name='get_predicted_data'),
]