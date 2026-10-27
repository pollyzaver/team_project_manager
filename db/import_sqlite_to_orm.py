"""Перенос данных из базы ПР7 (SQLite) в таблицы Django ORM.

Источник — data/teamproject.sqlite (его создаёт python -m db.import_json),
приёмник — база Django db.sqlite3 (на ней должны быть применены миграции).
Исходная база только читается и не изменяется.

Запуск из корня проекта: python -m db.import_sqlite_to_orm
"""
import os
import sqlite3
import sys
from datetime import date
from pathlib import Path
from typing import Optional

BASE_DIR = Path(__file__).resolve().parent.parent
SOURCE_DB = BASE_DIR / "data" / "teamproject.sqlite"


def parse_date(value: Optional[str]) -> Optional[date]:
    """Перевести строку ГГГГ-ММ-ДД в date (пустое значение — в None)."""
    if not value:
        return None
    return date.fromisoformat(value)


def read_source() -> dict:
    """Прочитать все таблицы исходной базы (только SELECT)."""
    if not SOURCE_DB.exists():
        raise FileNotFoundError(
            f"Исходная база не найдена: {SOURCE_DB}. "
            "Создайте её: python -m db.import_json"
        )
    with sqlite3.connect(SOURCE_DB) as connection:
        connection.row_factory = sqlite3.Row
        return {
            table: connection.execute(
                f"SELECT * FROM {table} ORDER BY id"
            ).fetchall()
            for table in ("projects", "teams", "members", "tasks")
        }


def main() -> None:
    """Перенести проекты, команды, участников и задачи через ORM."""
    sys.path.insert(0, str(BASE_DIR))
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "teamproject.settings")

    import django
    django.setup()

    # Модели импортируются только после django.setup().
    from django.db import transaction

    from project_pages.models import Project
    from task_pages.models import Task
    from team_pages.models import Member, Team

    source = read_source()

    # Одна транзакция: при ошибке изменения откатываются целиком.
    with transaction.atomic():
        # Порядок важен: сначала независимые таблицы, затем те, что
        # ссылаются на них внешними ключами. Исходные id сохраняются.
        for row in source["projects"]:
            Project.objects.update_or_create(
                pk=row["id"],
                defaults={
                    "name": row["name"],
                    "description": row["description"] or "",
                    "manager": row["manager"] or "",
                    "start_date": parse_date(row["start_date"]),
                    "end_date": parse_date(row["end_date"]),
                    "status": row["status"],
                },
            )
        for row in source["teams"]:
            Team.objects.update_or_create(
                pk=row["id"],
                defaults={
                    "name": row["name"],
                    "project_id": row["project_id"],
                },
            )
        for row in source["members"]:
            Member.objects.update_or_create(
                pk=row["id"],
                defaults={
                    "name": row["name"],
                    "role": row["role"] or "",
                    "team_id": row["team_id"],
                },
            )
        for row in source["tasks"]:
            Task.objects.update_or_create(
                pk=row["id"],
                defaults={
                    "name": row["name"],
                    "status": row["status"],
                    "due_date": parse_date(row["due_date"]),
                    "project_id": row["project_id"],
                    "assignee_id": row["assignee_id"],
                },
            )

    print("Перенос данных завершён.")
    print(f"Проектов: {Project.objects.count()}")
    print(f"Команд: {Team.objects.count()}")
    print(f"Участников: {Member.objects.count()}")
    print(f"Задач: {Task.objects.count()}")


if __name__ == "__main__":
    main()
