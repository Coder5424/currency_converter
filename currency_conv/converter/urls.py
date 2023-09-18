"""
URL mapping for converter app
"""
from django.urls import path
from .views import CurrencyConverterView

urlpatterns = [
    path('rates/', CurrencyConverterView.as_view(), name='converter'),
]