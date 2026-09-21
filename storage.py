"""Функции сохранения и загрузки данных проекта в формате JSON."""
import json
from typing import List, Optional, Tuple
from models import Member, Project, Task


def load_project_data(
    filename: str,
) -> Tuple[Optional[Project], List[Member]]:
    """Загрузить проект и участников команды из JSON-файла.

    Возвращает кортеж (project, members). Если файл не найден
    или содержит некорректный JSON, возвращается (None, []).
    """
    try:
        with open(filename, "r", encoding="utf-8") as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return None, []

    project_data = data.get("project")
    project = None
    if project_data:
        project = Project(
            name=project_data["name"],
            description=project_data["description"],
            manager=project_data["manager"],
            start_date=project_data["start_date"],
            end_date=project_data["end_date"],
            status=project_data["status"],
        )

    members = [
        Member(member["name"], member["role"])
        for member in data.get("members", [])
    ]
    return project, members


def save_project_data(
    filename: str,
    project: Project,
    members: List[Member],
) -> None:
    """Сохранить проект и участников команды в JSON-файл."""
    data = {
        "project": {
            "name": project.name,
            "description": project.description,
            "manager": project.manager,
            "start_date": project.start_date,
            "end_date": project.end_date,
            "status": project.status,
        },
        "members": [
            {"name": member.name, "role": member.role}
            for member in members
        ],
    }
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


def load_tasks(filename: str, members: List[Member]) -> List[Task]:
    """Загрузить задачи из JSON-файла, связав их с участниками.

    Если участник задачи не найден среди members, задача
    пропускается.
    """
    try:
        with open(filename, "r", encoding="utf-8") as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

    tasks = []
    for task_data in data:
        assignee = _find_member_by_name(members, task_data["assignee"])
        if assignee is None:
            continue
        tasks.append(Task(
            name=task_data["name"],
            status=task_data["status"],
            assignee=assignee,
        ))
    return tasks


def save_tasks(filename: str, tasks: List[Task]) -> None:
    """Сохранить задачи в JSON-файл."""
    data = [
        {
            "name": task.name,
            "status": task.status,
            "assignee": task.assignee.name,
        }
        for task in tasks
    ]
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