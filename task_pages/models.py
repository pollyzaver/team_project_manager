"""Модель задачи (Django ORM)."""
from django.db import models

from project_pages.models import Project
from team_pages.models import Member

# Подписи статусов для страницы задачи (как в классе Task из ПР3).
STATUS_TEXT = {
    "Выполнена": "Завершено",
    "В работе": "В процессе",
    "Новая": "Ожидает начала",
}


class Task(models.Model):
    """Задача проекта, назначенная участнику команды."""

    STATUS_NEW = "Новая"
    STATUS_IN_PROGRESS = "В работе"
    STATUS_DONE = "Выполнена"
    STATUS_CHOICES = [
        (STATUS_NEW, STATUS_NEW),
        (STATUS_IN_PROGRESS, STATUS_IN_PROGRESS),
        (STATUS_DONE, STATUS_DONE),
    ]

    name = models.CharField(
        max_length=200,
        verbose_name="Название",
    )
    status = models.CharField(
        max_length=50,
        choices=STATUS_CHOICES,
        default=STATUS_NEW,
        verbose_name="Статус",
    )
    # Срок необязателен: у задачи его может не быть (NULL).
    due_date = models.DateField(
        null=True,
        blank=True,
        verbose_name="Срок выполнения",
    )
    # PROTECT запрещает удалять проект или участника, пока на них
    # ссылаются задачи: так сохраняется история работы.
    project = models.ForeignKey(
        Project,
        on_delete=models.PROTECT,
        related_name="tasks",
        verbose_name="Проект",
    )
    assignee = models.ForeignKey(
        Member,
        on_delete=models.PROTECT,
        related_name="tasks",
        verbose_name="Исполнитель",
    )

    class Meta:
        ordering = ["pk"]
        verbose_name = "Задача"
        verbose_name_plural = "Задачи"

    def is_completed(self):
        """Проверить, выполнена ли задача (используется в шаблоне)."""
        return self.status == self.STATUS_DONE

    def get_status_text(self):
        """Вернуть статус задачи в читаемом виде."""
        return STATUS_TEXT.get(self.status, "Статус не определён")

    def complete(self):
        """Отметить задачу выполненной и сохранить только статус."""
        self.status = self.STATUS_DONE
        self.save(update_fields=["status"])

    def __str__(self):
        return self.name
