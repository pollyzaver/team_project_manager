"""Тесты для класса Member."""
from models import Member


def test_member_attributes():
    member = Member("Иван Иванов", "Разработчик")
    assert member.name == "Иван Иванов"
    assert member.role == "Разработчик"


def test_member_str():
    member = Member("Иван Иванов", "Разработчик")
    assert str(member) == "Иван Иванов - Разработчик"
