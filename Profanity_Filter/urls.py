from django.urls import path
from . import views

urlpatterns = [
    path('', views.Profanity, name='Profanity'),
]
