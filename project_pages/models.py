"""Модель проекта (Django ORM)."""
from django.db import models


class Project(models.Model):
    """Проект, которым управляет команда."""

    STATUS_ACTIVE = "Активен"
    STATUS_INACTIVE = "Не активен"
    STATUS_CHOICES = [
        (STATUS_ACTIVE, STATUS_ACTIVE),
        (STATUS_INACTIVE, STATUS_INACTIVE),
    ]

    name = models.CharField(
        max_length=200,
        verbose_name="Название",
    )
    description = models.TextField(
        blank=True,
        verbose_name="Описание",
    )
    manager = models.CharField(
        max_length=200,
        blank=True,
        verbose_name="Руководитель",
    )
    # Даты необязательны: в базе ПР7 они могли быть NULL.
    start_date = models.DateField(
        null=True,
        blank=True,
        verbose_name="Дата начала",
    )
    end_date = models.DateField(
        null=True,
        blank=True,
        verbose_name="Дата окончания",
    )
    status = models.CharField(
        max_length=50,
        choices=STATUS_CHOICES,
        default=STATUS_ACTIVE,
        verbose_name="Статус",
    )

    class Meta:
        ordering = ["name"]
        verbose_name = "Проект"
        verbose_name_plural = "Проекты"

    def is_active(self):
        """Проверить, активен ли проект (используется в шаблоне)."""
        return self.status == self.STATUS_ACTIVE

    def __str__(self):
        return self.name
