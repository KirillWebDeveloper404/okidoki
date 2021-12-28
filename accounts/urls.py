from django.contrib.auth import views
from django.urls import path
from .views import *

urlpatterns = [
    path('register/', register),
    path('registerClient/', registerClient),
    path('login/', loginView),
    path('logout/', logoutView)
]