"""Тесты для класса Team."""
from models import Member, Team


def make_team() -> Team:
    """Создать тестовую команду с одним участником."""
    return Team("Тестовая команда", [Member("Иван Иванов", "Разработчик")])


def test_team_str():
    team = make_team()
    assert str(team) == "Тестовая команда (1 участников)"


def test_team_default_members_empty():
    team = Team("Пустая команда")
    assert team.members == []


def test_team_add_member():
    team = Team("Команда", [])
    team.add_member(Member("Пётр Сидоров", "Тестировщик"))
    assert len(team.members) == 1
    assert team.members[0].name == "Пётр Сидоров"


def test_team_find_member():
    team = make_team()
    team.add_member(Member("Мария Смирнова", "Дизайнер"))
    found = team.find_member("смирнова")
    assert len(found) == 1
    assert found[0].name == "Мария Смирнова"


def test_team_find_member_not_found():
    team = make_team()
    assert team.find_member("Незнакомец") == []
