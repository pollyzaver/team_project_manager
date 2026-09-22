"""Функции сохранения и загрузки данных проектов в формате JSON."""
import json
from typing import List, Optional
from models import Member, Project, Task, Team


def load_project_data(filename: str) -> List[Project]:
    """Загрузить список проектов вместе с их командами из JSON-файла.

    Возвращает список объектов Project (в каждом уже есть team
    с участниками). Если файл не найден или содержит некорректный
    JSON, возвращается пустой список.
    """
    try:
        with open(filename, "r", encoding="utf-8") as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

    projects = []
    for project_data in data.get("projects", []):
        team_data = project_data.get("team", {})
        members = [
            Member(member["name"], member["role"])
            for member in team_data.get("members", [])
        ]
        team = Team(team_data.get("name", "Команда проекта"), members)
        projects.append(Project(
            name=project_data["name"],
            description=project_data["description"],
            manager=project_data["manager"],
            start_date=project_data["start_date"],
            end_date=project_data["end_date"],
            status=project_data["status"],
            team=team,
        ))
    return projects


def save_project_data(filename: str, projects: List[Project]) -> None:
    """Сохранить список проектов вместе с их командами в JSON-файл."""
    data = {
        "projects": [
            {
                "name": project.name,
                "description": project.description,
                "manager": project.manager,
                "start_date": project.start_date,
                "end_date": project.end_date,
                "status": project.status,
                "team": {
                    "name": project.team.name,
                    "members": [
                        {"name": member.name, "role": member.role}
                        for member in project.team.members
                    ],
                },
            }
            for project in projects
        ],
    }
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


def load_tasks(filename: str, projects: List[Project]) -> None:
    """Загрузить задачи из JSON-файла и разложить их по проектам.

    Задачи в файле хранятся отдельным словарём вида
    {"Название проекта": [задачи...]}. Результат записывается
    прямо в project.tasks у каждого проекта из списка.
    """
    try:
        with open(filename, "r", encoding="utf-8") as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        data = {}

    for project in projects:
        project.tasks = []
        for task_data in data.get(project.name, []):
            assignee = _find_member_by_name(
                project.team.members, task_data["assignee"],
            )
            if assignee is None:
                continue
            project.tasks.append(Task(
                name=task_data["name"],
                status=task_data["status"],
                assignee=assignee,
                due_date=task_data.get("due_date", ""),
            ))


def save_tasks(filename: str, projects: List[Project]) -> None:
    """Сохранить задачи всех проектов в JSON-файл (по названию проекта)."""
    data = {
        project.name: [
            {
                "name": task.name,
                "status": task.status,
                "assignee": task.assignee.name,
                "due_date": task.due_date,
            }
            for task in project.tasks
        ]
        for project in projects
    }
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


def _find_member_by_name(
    members: List[Member],
    name: str,
) -> Optional[Member]:
    """Найти участника по точному совпадению имени."""
    for member in members:
        if member.name == name:
            return member
    return None
