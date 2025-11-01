"""Game URL configuration."""

from django.urls import path
from . import views

app_name = 'game'

urlpatterns = [
    path('start/', views.start_view, name='start'),
    path('state/', views.state_view, name='state'),
    path('roll/', views.roll_view, name='roll'),
]