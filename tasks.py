"""Функции для работы с задачами проекта."""
from typing import List

from models import Member, Task


def add_task(
    tasks: List[Task],
    name: str,
    status: str,
    assignee: Member,
) -> None:
    """Добавить новую задачу в список задач."""
    tasks.append(Task(name, status, assignee))


def count_completed_tasks(tasks: List[Task]) -> int:
    """Подсчитать количество выполненных задач."""
    count = 0
    for task in tasks:
        if task.is_completed():
            count += 1
    return count


def calculate_progress(tasks: List[Task]) -> float:
    """Вычислить процент выполнения задач проекта."""
    if not tasks:
        return 0.0
    completed = count_completed_tasks(tasks)
    return (completed / len(tasks)) * 100


def filter_tasks_by_status(tasks: List[Task], status: str) -> List[Task]:
    """Отобрать задачи с указанным статусом."""
    return [task for task in tasks if task.status == status]


def sort_tasks_by_status(tasks: List[Task]) -> List[Task]:
    """Отсортировать задачи по статусу (по алфавиту)."""
    return sorted(tasks, key=lambda task: task.status)