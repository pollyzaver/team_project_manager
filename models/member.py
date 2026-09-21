"""Класс участника команды."""


class Member:
    """Участник команды проекта."""

    def __init__(self, name: str, role: str) -> None:
        """Создать объект участника команды."""
        self.name = name
        self.role = role

    def __str__(self) -> str:
        """Вернуть строковое представление участника."""
        return f"{self.name} - {self.role}"
