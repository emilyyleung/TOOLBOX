from django.urls import path
from . import views

urlpatterns = [
    path('', views.kraken_app, name='tool-kraken'),
]