"""Перенос данных из JSON-файлов в базу данных SQLite.

Запуск из корня проекта: python -m db.import_json
"""
from datetime import datetime
from typing import Optional

from db.database import DB_PATH, get_connection, init_db
from storage import load_all


def to_iso_date(value: str) -> Optional[str]:
    """Перевести дату из "ДД.ММ.ГГГГ" в "ГГГГ-ММ-ДД".

    Пустая или некорректная строка превращается в None (в базе NULL).
    Формат ГГГГ-ММ-ДД позволяет сравнивать и сортировать даты в SQL.
    """
    try:
        return datetime.strptime(value, "%d.%m.%Y").strftime("%Y-%m-%d")
    except (TypeError, ValueError):
        return None


def import_json() -> dict:
    """Заново заполнить таблицы данными из JSON и вернуть счётчики."""
    init_db()
    projects = load_all()
    connection = get_connection()
    counts = {"projects": 0, "teams": 0, "members": 0, "tasks": 0}
    try:
        # Повторный запуск не дублирует данные: сначала очищаем
        # таблицы в порядке от зависимых к главным.
        for table in ("tasks", "members", "teams", "projects"):
            connection.execute(f"DELETE FROM {table}")

        for project in projects:
            connection.execute(
                "INSERT INTO projects (id, name, description, manager, "
                "start_date, end_date, status) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (
                    project.id, project.name, project.description,
                    project.manager, to_iso_date(project.start_date),
                    to_iso_date(project.end_date), project.status,
                ),
            )
            counts["projects"] += 1

            team_id = connection.execute(
                "INSERT INTO teams (name, project_id) VALUES (?, ?)",
                (project.team.name, project.id),
            ).lastrowid
            counts["teams"] += 1

            # Участники в JSON не имеют id: база выдаёт их сама,
            # а мы запоминаем, какой id получил каждый участник.
            member_ids = {}
            for member in project.team.members:
                member_ids[id(member)] = connection.execute(
                    "INSERT INTO members (name, role, team_id) "
                    "VALUES (?, ?, ?)",
                    (member.name, member.role, team_id),
                ).lastrowid
                counts["members"] += 1

            for task in project.tasks:
                connection.execute(
                    "INSERT INTO tasks (id, name, status, due_date, "
                    "project_id, assignee_id) VALUES (?, ?, ?, ?, ?, ?)",
                    (
                        task.id, task.name, task.status,
                        to_iso_date(task.due_date), project.id,
                        member_ids[id(task.assignee)],
                    ),
                )
                counts["tasks"] += 1
        connection.commit()
    finally:
        connection.close()
    return counts


if __name__ == "__main__":
    result = import_json()
    print(f"Импорт завершён: {DB_PATH}")
    for table, count in result.items():
        print(f"  {table}: {count}")
