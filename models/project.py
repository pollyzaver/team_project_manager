"""Класс проекта."""


class Project:
    """Проект, которым управляет команда."""

    def __init__(
        self,
        name: str,
        description: str,
        manager: str,
        start_date: str,
        end_date: str,
        status: str,
        team=None,
        tasks=None,
    ) -> None:
        """Создать объект проекта.

        team — объект Team, назначенный на проект.
        tasks — список задач (Task), относящихся к проекту.
        """
        self.name = name
        self.description = description
        self.manager = manager
        self.start_date = start_date
        self.end_date = end_date
        self.status = status
        self.team = team
        self.tasks = tasks if tasks is not None else []

    def is_active(self) -> bool:
        """Проверить, активен ли проект."""
        return self.status == "Активен"

    def get_info_text(self) -> str:
        """Вернуть текстовое описание проекта."""
        text = (
            f"Название: {self.name}\n"
            f"Описание: {self.description}\n"
            f"Руководитель: {self.manager}\n"
            f"Дата начала: {self.start_date}\n"
            f"Дата окончания: {self.end_date}"
        )
        if self.team is not None:
            text += f"\nКоманда: {self.team}"
        return text

    def __str__(self) -> str:
        """Вернуть строковое представление проекта."""
        status_text = "Активен" if self.is_active() else "Не активен"
        return f"{self.name} ({status_text})"
