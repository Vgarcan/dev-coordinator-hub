"""URL routes owned by the dashboard application."""

from django.urls import path

from . import views


app_name = 'dashboard'

urlpatterns = [
    path('', views.home, name='home'),
    # Public-safe presentation only; never dispatches or approves work.
    path('tasks/', views.task_list, name='tasks'),
    # Fictional capability catalogue; no CLI or local LLM is queried.
    path('agents/', views.agent_gallery, name='agents'),
]
