from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    # path('register/',views.register,name='register'),
    path('login/',views.userlogin,name='login'),
    path('logout/',views.user_logout,name='logout'),
    path('profile/',views.profile,name='profile'),
    path('account/',views.UserAccountRegistrationView.as_view(),name='accountANDregister')
    
]