# demand_forecasting/urls.py

from django.urls import path
from . import views

app_name = 'demand_forecasting'

urlpatterns = [
    path('forecast/', views.forecast_view, name='forecast'),
]
