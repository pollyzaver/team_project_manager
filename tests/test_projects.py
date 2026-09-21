"""Тесты для класса Project, Member и функций projects.py."""
from models import Member, Project
from projects import add_member, find_member


def test_project_is_active():
    project = Project(
        name="Тестовый проект",
        description="Описание",
        manager="Иван Иванов",
        start_date="01.01.2026",
        end_date="01.02.2026",
        status="Активен",
    )
    assert project.is_active() is True


def test_project_is_not_active():
    project = Project(
        name="Тестовый проект",
        description="Описание",
        manager="Иван Иванов",
        start_date="01.01.2026",
        end_date="01.02.2026",
        status="Завершен",
    )
    assert project.is_active() is False


def test_project_str():
    project = Project(
        name="Тестовый проект",
        description="Описание",
        manager="Иван Иванов",
        start_date="01.01.2026",
        end_date="01.02.2026",
        status="Активен",
    )
    assert str(project) == "Тестовый проект (Активен)"


def test_add_member():
    members = []
    add_member(members, "Мария Смирнова", "Дизайнер")
    assert len(members) == 1
    assert isinstance(members[0], Member)
    assert members[0].name == "Мария Смирнова"
    assert members[0].role == "Дизайнер"


def test_find_member():
    members = [
        Member("Иван Иванов", "Разработчик"),
        Member("Мария Смирнова", "Дизайнер"),
    ]
    found = find_member(members, "иван")
    assert len(found) == 1
    assert found[0].name == "Иван Иванов"
