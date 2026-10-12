"""Тесты для функций-модулей из projects.py (не для классов)."""
from models import Member, Project, Team
from projects import (
    add_member,
    create_project,
    find_member,
    find_project,
    find_project_by_id,
    next_project_id,
)


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
    assert project.id == 1
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


def make_numbered_projects():
    """Создать два проекта с идентификаторами 1 и 2."""
    return [
        Project("Первый", "", "", "", "", "Активен", project_id=1),
        Project("Второй", "", "", "", "", "Активен", project_id=2),
    ]


def test_next_project_id_empty_list():
    assert next_project_id([]) == 1


def test_next_project_id_after_existing():
    assert next_project_id(make_numbered_projects()) == 3


def test_create_project_gets_next_id():
    projects = make_numbered_projects()
    project = create_project(
        projects, "Третий", "", "", "", "", "Команда",
    )
    assert project.id == 3


def test_find_project_by_id_found():
    found = find_project_by_id(make_numbered_projects(), 2)
    assert found is not None
    assert found.name == "Второй"


def test_find_project_by_id_not_found():
    assert find_project_by_id(make_numbered_projects(), 999) is None
