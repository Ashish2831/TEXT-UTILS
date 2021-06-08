from django.urls import path
from . import views

urlpatterns = [
    path('', views.TextExtracter, name='Extracter'),
]
