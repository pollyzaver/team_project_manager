"""Функции для работы с задачами проекта."""
from typing import List, Optional

from models import Member, Project, Task


def add_task(
    tasks: List[Task],
    name: str,
    status: str,
    assignee: Member,
    due_date: str = "",
    task_id: int = 0,
) -> None:
    """Добавить новую задачу в список задач.

    Если task_id не передан (0), идентификатор будет назначен
    при ближайшем сохранении данных (см. storage.save_tasks).
    """
    tasks.append(Task(name, status, assignee, due_date, task_id))


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


def sort_tasks_by_due_date(tasks: List[Task]) -> List[Task]:
    """Отсортировать задачи по сроку выполнения.

    Задачи без указанного срока уходят в конец списка.
    """
    return sorted(
        tasks,
        key=lambda task: (task.due_date == "", task.due_date),
    )


def update_task_status(tasks: List[Task], name: str, new_status: str) -> bool:
    """Найти задачу по имени и изменить её статус.

    Возвращает True, если задача найдена и статус обновлён,
    иначе False.
    """
    for task in tasks:
        if task.name == name:
            task.status = new_status
            return True
    return False


def delete_task(tasks: List[Task], name: str) -> bool:
    """Удалить задачу по имени.

    Возвращает True, если задача найдена и удалена, иначе False.
    """
    for index, task in enumerate(tasks):
        if task.name == name:
            del tasks[index]
            return True
    return False


def get_all_tasks(projects: List[Project]) -> List[Task]:
    """Собрать задачи всех проектов в один общий список."""
    all_tasks: List[Task] = []
    for project in projects:
        all_tasks.extend(project.tasks)
    return all_tasks


def find_task_by_id(tasks: List[Task], task_id: int) -> Optional[Task]:
    """Найти задачу по идентификатору.

    Возвращает объект Task или None, если задачи с таким
    идентификатором нет.
    """
    for task in tasks:
        if task.id == task_id:
            return task
    return None
