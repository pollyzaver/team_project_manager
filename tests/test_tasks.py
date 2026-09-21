"""Тесты для класса Task и функций tasks.py."""
from models import Member, Task
from tasks import (
    add_task,
    calculate_progress,
    count_completed_tasks,
    filter_tasks_by_status,
    sort_tasks_by_status,
)


def make_member() -> Member:
    """Создать тестового участника."""
    return Member("Иван Иванов", "Разработчик")


def test_task_is_completed():
    task = Task("Задача", "Выполнена", make_member())
    assert task.is_completed() is True


def test_task_is_not_completed():
    task = Task("Задача", "В работе", make_member())
    assert task.is_completed() is False


def test_add_task():
    tasks = []
    member = make_member()
    add_task(tasks, "Новая задача", "Новая", member)
    assert len(tasks) == 1
    assert isinstance(tasks[0], Task)
    assert tasks[0].assignee is member


def test_count_completed_tasks():
    member = make_member()
    tasks = [
        Task("Задача 1", "Выполнена", member),
        Task("Задача 2", "В работе", member),
        Task("Задача 3", "Выполнена", member),
    ]
    assert count_completed_tasks(tasks) == 2


def test_calculate_progress():
    member = make_member()
    tasks = [
        Task("Задача 1", "Выполнена", member),
        Task("Задача 2", "Новая", member),
    ]
    assert calculate_progress(tasks) == 50.0


def test_filter_tasks_by_status():
    member = make_member()
    tasks = [
        Task("Задача 1", "Выполнена", member),
        Task("Задача 2", "Новая", member),
    ]
    filtered = filter_tasks_by_status(tasks, "Новая")
    assert len(filtered) == 1
    assert filtered[0].name == "Задача 2"


def test_sort_tasks_by_status():
    member = make_member()
    tasks = [
        Task("Задача 1", "Новая", member),
        Task("Задача 2", "Выполнена", member),
    ]
    sorted_tasks = sort_tasks_by_status(tasks)
    assert sorted_tasks[0].status == "Выполнена"
