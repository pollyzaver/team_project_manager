"""Маршруты приложения report_pages (префикс reports/)."""
from django.urls import path

from . import views

app_name = "reports"

urlpatterns = [
    path("", views.stats, name="stats"),
    path("projects/", views.projects, name="projects"),
    path("tasks/", views.tasks, name="tasks"),
    path("deadlines/", views.deadlines, name="deadlines"),
    path("workload/", views.workload, name="workload"),
]
