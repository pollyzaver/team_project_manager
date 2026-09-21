"""Функции для работы с задачами проекта."""


def get_task_status_text(status: str) -> str:
    """Преобразовать статус задачи в читаемый текст."""
    statuses = {
        "Выполнена": "Завершено",
        "В работе": "В процессе",
        "Новая": "Ожидает начала",
    }
    return statuses.get(status, "Статус не определен")


def add_task(tasks: list, name: str, status: str, assignee: str) -> None:
    """Добавить новую задачу в список задач."""
    tasks.append({"name": name, "status": status, "assignee": assignee})


def count_completed_tasks(tasks: list) -> int:
    """Подсчитать количество выполненных задач."""
    count = 0
    for task in tasks:
        if task["status"] == "Выполнена":
            count += 1
    return count


def calculate_progress(tasks: list) -> float:
    """Вычислить процент выполнения задач проекта."""
    if not tasks:
        return 0.0
    completed = count_completed_tasks(tasks)
    return (completed / len(tasks)) * 100


def filter_tasks_by_status(tasks: list, status: str) -> list:
    """Отобрать задачи с указанным статусом."""
    return [task for task in tasks if task["status"] == status]


def sort_tasks_by_status(tasks: list) -> list:
    """Отсортировать задачи по статусу (по алфавиту)."""
    return sorted(tasks, key=lambda task: task["status"])
