from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('main/', views.main, name='mainPage'),
    path('colloquial/', views.colloquial, name='colloquial'),
    path('exercise/', views.exercise, name='exercise'),
    path('greetings/', views.greetings, name='greetings'),
    path('hospital/', views.hospital, name='hospital'),
    path('howto/', views.howto, name='howto'),
    path('practice/', views.practice, name='practice'),
    path('restaurant/', views.restaurant, name='restaurant'),
    path('school/', views.school, name='school'),
    path('shopping/', views.shopping, name='shopping'),
    path('tonguetwister/', views.tonguetwister, name='tonguetwister'),
    path('travel/', views.travel, name='travel'),
]
