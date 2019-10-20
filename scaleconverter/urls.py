from django.urls import path
from . import views

urlpatterns = [
    path('', views.scale_app, name='tool-scaleconverter'),
]