"""Тесты для функций-модулей из tasks.py (не для класса Task)."""
from models import Member, Project, Task
from tasks import (
    add_task,
    calculate_progress,
    count_completed_tasks,
    delete_task,
    filter_tasks_by_status,
    find_task_by_id,
    get_all_tasks,
    sort_tasks_by_due_date,
    sort_tasks_by_status,
    update_task_status,
)


def make_member() -> Member:
    """Создать тестового участника."""
    return Member("Иван Иванов", "Разработчик")


def test_add_task():
    tasks = []
    member = make_member()
    add_task(tasks, "Новая задача", "Новая", member)
    assert len(tasks) == 1
    assert isinstance(tasks[0], Task)
    assert tasks[0].assignee is member
    assert tasks[0].due_date == ""
    assert tasks[0].id == 0


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


def test_sort_tasks_by_due_date_puts_undated_last():
    member = make_member()
    tasks = [
        Task("Без срока", "Новая", member),
        Task("Позже", "Новая", member, due_date="01.12.2026"),
        Task("Раньше", "Новая", member, due_date="01.10.2026"),
    ]
    sorted_tasks = sort_tasks_by_due_date(tasks)
    assert [task.name for task in sorted_tasks] == [
        "Раньше", "Позже", "Без срока",
    ]


def test_update_task_status_found():
    member = make_member()
    tasks = [Task("Задача", "Новая", member)]
    assert update_task_status(tasks, "Задача", "В работе") is True
    assert tasks[0].status == "В работе"


def test_update_task_status_not_found():
    tasks = []
    assert update_task_status(tasks, "Нет такой", "В работе") is False


def test_delete_task_found():
    member = make_member()
    tasks = [
        Task("Задача 1", "Новая", member),
        Task("Задача 2", "Новая", member),
    ]
    assert delete_task(tasks, "Задача 1") is True
    assert len(tasks) == 1
    assert tasks[0].name == "Задача 2"


def test_delete_task_not_found():
    tasks = [Task("Задача 1", "Новая", make_member())]
    assert delete_task(tasks, "Нет такой") is False
    assert len(tasks) == 1


def test_get_all_tasks_joins_tasks_of_all_projects():
    member = make_member()
    first = Project("Первый", "", "", "", "", "Активен", tasks=[
        Task("Задача 1", "Новая", member, task_id=1),
    ])
    second = Project("Второй", "", "", "", "", "Активен", tasks=[
        Task("Задача 2", "Новая", member, task_id=2),
        Task("Задача 3", "Новая", member, task_id=3),
    ])
    all_tasks = get_all_tasks([first, second])
    assert [task.id for task in all_tasks] == [1, 2, 3]


def test_find_task_by_id_found():
    tasks = [
        Task("Задача 1", "Новая", make_member(), task_id=1),
        Task("Задача 2", "Новая", make_member(), task_id=2),
    ]
    found = find_task_by_id(tasks, 2)
    assert found is not None
    assert found.name == "Задача 2"


def test_find_task_by_id_not_found():
    tasks = [Task("Задача 1", "Новая", make_member(), task_id=1)]
    assert find_task_by_id(tasks, 999) is None
