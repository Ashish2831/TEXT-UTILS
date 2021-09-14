from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home, name='Home'),
    path('features/', views.Features, name='Features'),
    path('about/', views.About, name='About'),
    path('contact/', views.Contact, name='Contact'),
    path('login/', views.Login, name='Login'),
    path('logout/', views.Logout, name='Logout'),
    path('register/', views.Register, name="Register"),
    path('delete_user/<int:id>/', views.Delete_User, name="Delete_User"),
    path('remove/<int:id>/', views.Remove_Profile_Picure, name="Remove"),
    path('dashboard/<int:id>/', views.Dashboard, name="Dashboard"),
    path('password_change/', views.Password_Change, name="Password_Change"),
    path('password_reset/', views.PasswordReset, name="Reset"),
    path('reset_done/', views.ResetDone, name="ResetDone"),
    path('google/', views.Google, name="Google"),
]
