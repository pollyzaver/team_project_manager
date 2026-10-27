"""Модели команды и участника (Django ORM)."""
from django.db import models

from project_pages.models import Project


class Team(models.Model):
    """Команда, назначенная на проект (у проекта одна команда)."""

    name = models.CharField(
        max_length=200,
        verbose_name="Название команды",
    )
    # Связь «один к одному»: project.team — команда проекта.
    # Команда не существует без проекта, поэтому CASCADE.
    project = models.OneToOneField(
        Project,
        on_delete=models.CASCADE,
        related_name="team",
        verbose_name="Проект",
    )

    class Meta:
        ordering = ["name"]
        verbose_name = "Команда"
        verbose_name_plural = "Команды"

    def __str__(self):
        return self.name


class Member(models.Model):
    """Участник команды проекта."""

    name = models.CharField(
        max_length=200,
        verbose_name="Имя",
    )
    role = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Роль",
    )
    # Связь «многие к одному»: team.members — участники команды.
    team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        related_name="members",
        verbose_name="Команда",
    )

    class Meta:
        ordering = ["name"]
        verbose_name = "Участник"
        verbose_name_plural = "Участники"

    def __str__(self):
        return f"{self.name} – {self.role}" if self.role else self.name
