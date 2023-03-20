from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('dashboard/', dashboard, name='dashboard'),
    path('signin/', signin, name='signin'),
    path('logout/', logout, name='logout'),
    path('dashboard/file/<id>/', readfile, name='readfile'),
]