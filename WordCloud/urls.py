from django.urls import path
from . import views

urlpatterns = [
    path('', views.wordCloud, name='WordCloud'),
    path('addwords/', views.AddWords, name='AddWords'),
    path('delete/<int:index>', views.delete_word, name='Delete_Word'),
    path('generatewords/', views.GenerateWords, name='GenerateWords'),
    path('generatetext/', views.GenerateText, name='GenerateText'),
    path('generatefile/', views.GenerateFile, name='GenerateFile'),
]
