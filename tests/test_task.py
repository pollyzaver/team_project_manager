"""Тесты для класса Task."""
from models import Member, Task


def make_member() -> Member:
    """Создать тестового участника."""
    return Member("Иван Иванов", "Разработчик")


def test_task_is_completed():
    task = Task("Задача", "Выполнена", make_member())
    assert task.is_completed() is True


def test_task_is_not_completed():
    task = Task("Задача", "В работе", make_member())
    assert task.is_completed() is False


def test_task_get_status_text_known():
    task = Task("Задача", "Новая", make_member())
    assert task.get_status_text() == "Ожидает начала"


def test_task_get_status_text_unknown():
    task = Task("Задача", "Что-то странное", make_member())
    assert task.get_status_text() == "Статус не определен"


def test_task_due_date_default_empty():
    task = Task("Задача", "Новая", make_member())
    assert task.due_date == ""


def test_task_str_without_due_date():
    task = Task("Задача", "Новая", make_member())
    assert str(task) == "Задача [Ожидает начала] - Иван Иванов"


def test_task_str_with_due_date():
    task = Task("Задача", "Новая", make_member(), due_date="05.10.2026")
    assert str(task) == (
        "Задача [Ожидает начала] - Иван Иванов, срок: 05.10.2026"
    )
