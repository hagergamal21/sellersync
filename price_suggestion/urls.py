# price_suggestion/urls.py

from django.urls import path
from . import views

app_name = 'price_suggestion'

urlpatterns = [
    path('predict-price/', views.predict_price_and_save, name='predict_price_and_save'),
    path('form/', views.price_suggestion_form, name='price_suggestion_form'),
    path('history/', views.prediction_history, name='prediction_history'),
]
