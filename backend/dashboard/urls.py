"""URL routes owned by the dashboard application."""

from django.urls import path

from . import views


app_name = 'dashboard'

urlpatterns = [
    path('', views.home, name='home'),
]
