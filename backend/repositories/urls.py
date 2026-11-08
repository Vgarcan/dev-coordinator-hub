"""URL routes owned by the repositories application."""

from django.urls import path

from . import views


app_name = 'repositories'

urlpatterns = [
    path('', views.repository_list, name='list'),
]
