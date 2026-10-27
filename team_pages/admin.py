"""Регистрация моделей приложения team_pages в админ-панели."""
from django.contrib import admin

from team_pages.models import Member, Team


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    """Команды в админ-панели."""

    list_display = ("name", "project")


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    """Участники в админ-панели."""

    list_display = ("name", "role", "team")
    list_filter = ("role",)
    search_fields = ("name",)
