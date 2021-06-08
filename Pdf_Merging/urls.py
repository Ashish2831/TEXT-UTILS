from django.urls import path
from . import views

urlpatterns = [
    path('upload', views.Upload, name='Upload'),
    path('merge', views.Merge, name='MergePDFs'),
]
