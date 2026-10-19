"""Подключение к базе данных SQLite проекта TeamProject Manager."""
import os
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
# Путь к базе можно переопределить переменной окружения TEAMPROJECT_DB.
DB_PATH = Path(os.environ.get(
    "TEAMPROJECT_DB", BASE_DIR / "data" / "teamproject.sqlite",
))
SCHEMA_PATH = BASE_DIR / "sql" / "schema.sql"


def get_connection(db_path: Path = DB_PATH) -> sqlite3.Connection:
    """Открыть соединение с базой данных.

    Строки результата возвращаются как sqlite3.Row: к полям можно
    обращаться по имени (row["name"]), а в шаблоне — {{ row.name }}.
    Внешние ключи в SQLite по умолчанию отключены, поэтому их
    проверку включаем для каждого соединения.
    """
    connection = sqlite3.connect(db_path)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def init_db(db_path: Path = DB_PATH) -> None:
    """Создать файл базы данных и таблицы из sql/schema.sql."""
    schema = SCHEMA_PATH.read_text(encoding="utf-8")
    connection = get_connection(db_path)
    try:
        connection.executescript(schema)
        connection.commit()
    finally:
        connection.close()


def fetch_all(sql: str, params: tuple = ()) -> list:
    """Выполнить SELECT-запрос и вернуть все строки результата.

    Значения передаются отдельно от текста запроса через ? —
    так SQLite сам подставляет их безопасно (защита от SQL-инъекций).
    """
    if not DB_PATH.exists():
        raise FileNotFoundError(
            "База данных не создана. Выполните: python -m db.import_json"
        )
    connection = get_connection()
    try:
        return connection.execute(sql, params).fetchall()
    finally:
        connection.close()


def fetch_one(sql: str, params: tuple = ()):
    """Выполнить SELECT-запрос и вернуть первую строку (или None)."""
    rows = fetch_all(sql, params)
    return rows[0] if rows else None


if __name__ == "__main__":
    init_db()
    print(f"База данных создана: {DB_PATH}")
