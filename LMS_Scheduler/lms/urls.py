from django.contrib import admin
from django.urls import path
from . import views
import account
urlpatterns = [
    path('/', views.home, name = "home"),

]
