"""Функции для работы с проектом и участниками команды."""


def get_project_info_text(project: dict) -> str:
    """Вернуть текстовое описание проекта."""
    return (
        f"Название: {project['name']}\n"
        f"Описание: {project['description']}\n"
        f"Руководитель: {project['manager']}\n"
        f"Дата начала: {project['start_date']}\n"
        f"Дата окончания: {project['end_date']}"
    )


def is_project_active(project: dict) -> bool:
    """Проверить, активен ли проект."""
    return project["status"] == "Активен"


def add_member(members: list, name: str, role: str) -> None:
    """Добавить участника в список участников команды."""
    members.append({"name": name, "role": role})


def find_member(members: list, query: str) -> list:
    """Найти участников по подстроке имени."""
    return [
        member for member in members
        if query.lower() in member["name"].lower()
    ]
