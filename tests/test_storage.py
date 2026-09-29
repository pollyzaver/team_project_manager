"""Тесты для функций сохранения/загрузки данных в storage.py."""
from models import Member, Project, Task, Team
from storage import (
    load_project_data,
    load_tasks,
    save_project_data,
    save_tasks,
)


def make_project(name: str = "Тестовый проект") -> Project:
    """Создать тестовый проект с командой из двух участников."""
    team = Team("Тестовая команда", [
        Member("Иван Иванов", "Разработчик"),
        Member("Мария Смирнова", "Дизайнер"),
    ])
    return Project(
        name=name,
        description="Описание",
        manager="Анна Петрова",
        start_date="01.01.2026",
        end_date="01.02.2026",
        status="Активен",
        team=team,
    )


def test_save_and_load_project_data_roundtrip(tmp_path):
    filename = tmp_path / "projects.json"
    project = make_project()

    save_project_data(str(filename), [project])
    loaded = load_project_data(str(filename))

    assert len(loaded) == 1
    loaded_project = loaded[0]
    assert loaded_project.name == project.name
    assert loaded_project.status == "Активен"
    assert loaded_project.team.name == "Тестовая команда"
    assert [m.name for m in loaded_project.team.members] == [
        "Иван Иванов", "Мария Смирнова",
    ]


def test_load_project_data_missing_file_returns_empty_list(tmp_path):
    filename = tmp_path / "does_not_exist.json"
    assert load_project_data(str(filename)) == []


def test_load_project_data_invalid_json_returns_empty_list(tmp_path):
    filename = tmp_path / "broken.json"
    filename.write_text("это не json", encoding="utf-8")
    assert load_project_data(str(filename)) == []


def test_save_and_load_tasks_roundtrip(tmp_path):
    filename = tmp_path / "tasks.json"
    project = make_project()
    ivan = project.team.members[0]
    project.tasks = [Task("Задача 1", "Новая", ivan, due_date="10.10.2026")]

    save_tasks(str(filename), [project])

    reloaded_project = make_project()
    load_tasks(str(filename), [reloaded_project])

    assert len(reloaded_project.tasks) == 1
    task = reloaded_project.tasks[0]
    assert task.name == "Задача 1"
    assert task.assignee.name == "Иван Иванов"
    assert task.due_date == "10.10.2026"


def test_load_tasks_skips_task_with_unknown_assignee(tmp_path):
    filename = tmp_path / "tasks.json"
    filename.write_text(
        '{"Тестовый проект": ['
        '{"name": "Задача", "status": "Новая", '
        '"assignee": "Незнакомец", "due_date": ""}'
        ']}',
        encoding="utf-8",
    )
    project = make_project()

    load_tasks(str(filename), [project])

    assert project.tasks == []


def test_load_tasks_missing_file_sets_empty_task_lists(tmp_path):
    filename = tmp_path / "does_not_exist.json"
    project = make_project()

    load_tasks(str(filename), [project])

    assert project.tasks == []


def test_tasks_are_grouped_by_project_name(tmp_path):
    filename = tmp_path / "tasks.json"
    project_a = make_project("Проект А")
    project_b = make_project("Проект Б")
    project_a.tasks = [
        Task("Задача А", "Новая", project_a.team.members[0]),
    ]
    project_b.tasks = [
        Task("Задача Б", "Выполнена", project_b.team.members[1]),
    ]

    save_tasks(str(filename), [project_a, project_b])

    reloaded_a = make_project("Проект А")
    reloaded_b = make_project("Проект Б")
    load_tasks(str(filename), [reloaded_a, reloaded_b])

    assert [t.name for t in reloaded_a.tasks] == ["Задача А"]
    assert [t.name for t in reloaded_b.tasks] == ["Задача Б"]
