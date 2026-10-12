"""Класс задачи проекта."""

STATUS_TEXT = {
    "Выполнена": "Завершено",
    "В работе": "В процессе",
    "Новая": "Ожидает начала",
}


class Task:
    """Задача проекта."""

    def __init__(
        self,
        name: str,
        status: str,
        assignee,
        due_date: str = "",
        task_id: int = 0,
    ) -> None:
        """Создать объект задачи.

        assignee — объект Member, ответственный за выполнение задачи.
        due_date — срок выполнения в формате "ДД.ММ.ГГГГ" (может быть
        пустой строкой, если срок не задан).
        task_id — уникальный числовой идентификатор задачи
        (используется в адресах веб-страниц, например /tasks/1/).
        """
        self.id = task_id
        self.name = name
        self.status = status
        self.assignee = assignee
        self.due_date = due_date

    def is_completed(self) -> bool:
        """Проверить, выполнена ли задача."""
        return self.status == "Выполнена"

    def get_status_text(self) -> str:
        """Вернуть статус задачи в читаемом виде."""
        return STATUS_TEXT.get(self.status, "Статус не определен")

    def __str__(self) -> str:
        """Вернуть строковое представление задачи."""
        due_text = f", срок: {self.due_date}" if self.due_date else ""
        return (
            f"{self.name} [{self.get_status_text()}] "
            f"- {self.assignee.name}{due_text}"
        )
