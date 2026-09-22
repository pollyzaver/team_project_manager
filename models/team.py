"""Класс команды проекта."""


class Team:
    """Команда, объединяющая участников для работы над проектом."""

    def __init__(self, name: str, members=None) -> None:
        """Создать команду с именем и списком участников (Member)."""
        self.name = name
        self.members = members if members is not None else []

    def add_member(self, member) -> None:
        """Добавить участника в команду."""
        self.members.append(member)

    def find_member(self, query: str):
        """Найти участников команды по подстроке имени."""
        return [
            member for member in self.members
            if query.lower() in member.name.lower()
        ]

    def __str__(self) -> str:
        """Вернуть строковое представление команды."""
        return f"{self.name} ({len(self.members)} участников)"
