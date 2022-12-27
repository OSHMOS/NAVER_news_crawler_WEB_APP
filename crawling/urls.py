from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('crawling/', views.crawling, name='crawling'),
    path('greeting/', views.greeting, name='greeting'),
    path('export/', views.export, name='export'),
]
