from tasks import (
    add_task,
    count_completed_tasks,
    calculate_progress,
    get_task_status_text,
)


def test_add_task():
    tasks = []
    add_task(tasks, "Тестовая задача", "Новая", "Иван Иванов")
    assert len(tasks) == 1


def test_count_completed_tasks():
    tasks = [
        {"name": "A", "status": "Выполнена", "assignee": "X"},
        {"name": "B", "status": "Новая", "assignee": "Y"},
    ]
    assert count_completed_tasks(tasks) == 1


def test_calculate_progress():
    tasks = [
        {"name": "A", "status": "Выполнена", "assignee": "X"},
        {"name": "B", "status": "Выполнена", "assignee": "Y"},
    ]
    assert calculate_progress(tasks) == 100.0


def test_get_task_status_text():
    assert get_task_status_text("Новая") == "Ожидает начала"
