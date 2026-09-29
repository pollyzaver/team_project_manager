"""Тесты для класса Project."""
from models import Member, Project, Team


def make_team() -> Team:
    """Создать тестовую команду с одним участником."""
    return Team("Тестовая команда", [Member("Иван Иванов", "Разработчик")])


def make_project(status: str = "Активен", team=None) -> Project:
    """Создать тестовый проект."""
    return Project(
        name="Тестовый проект",
        description="Описание",
        manager="Анна Петрова",
        start_date="01.01.2026",
        end_date="01.02.2026",
        status=status,
        team=team,
    )


def test_project_is_active():
    assert make_project(status="Активен", team=make_team()).is_active() is True


def test_project_is_not_active():
    project = make_project(status="Завершен", team=make_team())
    assert project.is_active() is False


def test_project_str():
    project = make_project(status="Активен", team=make_team())
    assert str(project) == "Тестовый проект (Активен)"


def test_project_tasks_default_empty():
    project = make_project(team=make_team())
    assert project.tasks == []


def test_project_team_default_none():
    project = make_project()
    assert project.team is None


def test_project_get_info_text_includes_team():
    project = make_project(team=make_team())
    info = project.get_info_text()
    assert "Команда: Тестовая команда (1 участников)" in info


def test_project_get_info_text_without_team():
    project = make_project()
    info = project.get_info_text()
    assert "Команда" not in info
