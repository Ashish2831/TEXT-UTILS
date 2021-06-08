from django.urls import path
from . import views

urlpatterns = [
    path('', views.SpeechRecognition, name='BrowserVoice'),
    path('browser_voice', views.BrowserVoice, name='SpeechRecognition'),
]
