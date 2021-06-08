from django.urls import path
from . import views

urlpatterns = [
    path('', views.Audio_Transcribing, name="Audio_Transcribing")
]
