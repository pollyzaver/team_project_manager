"""Регистрация моделей приложения project_pages в админ-панели."""
from django.contrib import admin

from project_pages.models import Project


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    """Проекты в админ-панели."""

    list_display = ("name", "manager", "status", "start_date", "end_date")
    list_filter = ("status",)
    search_fields = ("name", "manager")
