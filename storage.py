"""Функции сохранения и загрузки данных проекта в формате JSON."""
import json


def load_data(filename: str, default: object) -> object:
    """Загрузить данные из JSON-файла.

    Если файл не найден или содержит некорректный JSON,
    возвращается значение default.
    """
    try:
        with open(filename, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return default
    except json.JSONDecodeError:
        return default


def save_data(filename: str, data: object) -> None:
    """Сохранить данные в JSON-файл."""
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
