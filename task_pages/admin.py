"""Регистрация моделей приложения task_pages в админ-панели."""
from django.contrib import admin

from task_pages.models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    """Задачи в админ-панели."""

    list_display = ("name", "project", "assignee", "status", "due_date")
    list_filter = ("status", "project")
    search_fields = ("name",)
