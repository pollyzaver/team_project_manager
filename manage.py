#!/usr/bin/env python
"""Утилита командной строки Django для административных задач."""
import os
import sys


def main():
    """Запустить административные задачи."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "teamproject.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Не удалось импортировать Django. Установлен ли он и "
            "активировано ли виртуальное окружение?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
