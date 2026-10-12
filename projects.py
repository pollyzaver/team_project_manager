"""Функции для работы с проектами, командами и участниками."""
from typing import List, Optional

from models import Member, Project, Team


def add_member(members: List[Member], name: str, role: str) -> None:
    """Добавить участника в список участников команды."""
    members.append(Member(name, role))


def find_member(members: List[Member], query: str) -> List[Member]:
    """Найти участников по подстроке имени."""
    return [
        member for member in members
        if query.lower() in member.name.lower()
    ]


def create_project(
    projects: List[Project],
    name: str,
    description: str,
    manager: str,
    start_date: str,
    end_date: str,
    team_name: str,
) -> Project:
    """Создать новый проект с пустой командой и добавить его в список.

    Новый проект создаётся со статусом "Активен" и командой без
    участников — участников добавляют отдельно через add_member.
    """
    project = Project(
        project_id=next_project_id(projects),
        name=name,
        description=description,
        manager=manager,
        start_date=start_date,
        end_date=end_date,
        status="Активен",
        team=Team(team_name, []),
    )
    projects.append(project)
    return project


def find_project(projects: List[Project], query: str) -> List[Project]:
    """Найти проекты по подстроке названия."""
    return [
        project for project in projects
        if query.lower() in project.name.lower()
    ]


def next_project_id(projects: List[Project]) -> int:
    """Вернуть следующий свободный числовой идентификатор проекта."""
    return max((project.id for project in projects), default=0) + 1


def find_project_by_id(
    projects: List[Project],
    project_id: int,
) -> Optional[Project]:
    """Найти проект по идентификатору.

    Возвращает объект Project или None, если проекта с таким
    идентификатором нет.
    """
    for project in projects:
        if project.id == project_id:
            return project
    return None
