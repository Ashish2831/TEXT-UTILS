from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.Summarizer, name='Summarizer'),
    path('text/', views.Summarize_Text, name='Summarize_Text'),
    path('file/', views.Summarize_File, name='Summarize_File'),
]
