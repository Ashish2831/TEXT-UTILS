from django.urls import path
from . import views

urlpatterns = [
    path('', views.Sentiment, name='Sentiment'),
    path('multiple/', views.Sentiment_Multiple, name='SentimentMultiple'),
]
