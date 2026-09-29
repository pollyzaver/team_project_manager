"""Тесты для функций-модулей из projects.py (не для классов)."""
from models import Member, Project, Team
from projects import add_member, create_project, find_member, find_project


def make_team() -> Team:
    """Создать тестовую команду с одним участником."""
    return Team("Тестовая команда", [Member("Иван Иванов", "Разработчик")])


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


def test_create_project():
    projects = []
    project = create_project(
        projects,
        name="Новый проект",
        description="Описание",
        manager="Анна Петрова",
        start_date="01.01.2027",
        end_date="01.06.2027",
        team_name="Новая команда",
    )
    assert len(projects) == 1
    assert isinstance(project, Project)
    assert project.status == "Активен"
    assert project.team.name == "Новая команда"
    assert project.team.members == []


def test_find_project():
    projects = [
        Project(
            name="Мобильное приложение",
            description="",
            manager="",
            start_date="",
            end_date="",
            status="Активен",
            team=make_team(),
        ),
        Project(
            name="Веб-сайт",
            description="",
            manager="",
            start_date="",
            end_date="",
            status="Активен",
            team=make_team(),
        ),
    ]
    found = find_project(projects, "мобильное")
    assert len(found) == 1
    assert found[0].name == "Мобильное приложение"
