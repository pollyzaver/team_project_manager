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
    try:
        # Повторный запуск не дублирует данные: сначала очищаем
        # таблицы в порядке от зависимых к главным.
        for table in ("tasks", "members", "teams", "projects"):
            connection.execute(f"DELETE FROM {table}")

        projects_rows, teams_rows, members_rows, tasks_rows = [], [], [], []
        next_member_id = 1
        for team_id, project in enumerate(projects, start=1):
            projects_rows.append((
                project.id, project.name, project.description,
                project.manager, to_iso_date(project.start_date),
                to_iso_date(project.end_date), project.status,
            ))
            teams_rows.append((team_id, project.team.name, project.id))

            # Участники в JSON не имеют id: назначаем их сами и
            # запоминаем, какой id получил каждый участник.
            member_ids = {}
            for member in project.team.members:
                member_ids[id(member)] = next_member_id
                members_rows.append(
                    (next_member_id, member.name, member.role, team_id),
                )
                next_member_id += 1

            for task in project.tasks:
                tasks_rows.append((
                    task.id, task.name, task.status,
                    to_iso_date(task.due_date), project.id,
                    member_ids[id(task.assignee)],
                ))

        # executemany выполняет один запрос сразу для всех наборов
        # значений. Порядок важен: сначала главные таблицы, потом
        # те, что на них ссылаются (внешние ключи).
        connection.executemany(
            "INSERT INTO projects (id, name, description, manager, "
            "start_date, end_date, status) VALUES (?, ?, ?, ?, ?, ?, ?)",
            projects_rows,
        )
        connection.executemany(
            "INSERT INTO teams (id, name, project_id) VALUES (?, ?, ?)",
            teams_rows,
        )
        connection.executemany(
            "INSERT INTO members (id, name, role, team_id) "
            "VALUES (?, ?, ?, ?)",
            members_rows,
        )
        connection.executemany(
            "INSERT INTO tasks (id, name, status, due_date, "
            "project_id, assignee_id) VALUES (?, ?, ?, ?, ?, ?)",
            tasks_rows,
        )
        counts = {
            "projects": len(projects_rows),
            "teams": len(teams_rows),
            "members": len(members_rows),
            "tasks": len(tasks_rows),
        }
        connection.commit()
    finally:
        connection.close()
    return counts


if __name__ == "__main__":
    result = import_json()
    print(f"Импорт завершён: {DB_PATH}")
    for table, count in result.items():
        print(f"  {table}: {count}")
