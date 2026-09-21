"""Функции для работы с участниками команды."""
from typing import List

from models import Member


def add_member(members: List[Member], name: str, role: str) -> None:
    """Добавить участника в список участников команды."""
    members.append(Member(name, role))


def find_member(members: List[Member], query: str) -> List[Member]:
    """Найти участников по подстроке имени."""
    return [
        member for member in members
        if query.lower() in member.name.lower()
    ]