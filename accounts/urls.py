from django.contrib.auth import views
from django.urls import path
from .views import *

urlpatterns = [
    path('register/', register),
    path('registerClient/', registerClient),
    path('login/<str:next>/<str:page>', loginView, name='login'),
    path('login/<str:next>', loginView, name='loginNext'),
    path('login/', loginView, name='BaseLogin'),
    path('logout/', logoutView)
]