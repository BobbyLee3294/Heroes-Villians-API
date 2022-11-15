from django.urls import path
from . import views

urlpatterns = [
    path('', views.supers_list), # views.supers_list, optional params
    path('<int:pk>/', views.super_detail), # views.supers_details
]