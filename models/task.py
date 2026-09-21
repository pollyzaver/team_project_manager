"""Класс задачи проекта."""

STATUS_TEXT = {
    "Выполнена": "Завершено",
    "В работе": "В процессе",
    "Новая": "Ожидает начала",
}


class Task:
    """Задача проекта."""

    def __init__(self, name: str, status: str, assignee) -> None:
        """Создать объект задачи.

        assignee — объект Member, ответственный за выполнение задачи.
        """
        self.name = name
        self.status = status
        self.assignee = assignee

    def is_completed(self) -> bool:
        """Проверить, выполнена ли задача."""
        return self.status == "Выполнена"

    def get_status_text(self) -> str:
        """Вернуть статус задачи в читаемом виде."""
        return STATUS_TEXT.get(self.status, "Статус не определен")

    def __str__(self) -> str:
        """Вернуть строковое представление задачи."""
        return (
            f"{self.name} [{self.get_status_text()}] "
            f"- {self.assignee.name}"
        )
