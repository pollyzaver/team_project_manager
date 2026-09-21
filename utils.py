"""Вспомогательные функции ввода данных с обработкой ошибок."""


def input_int(prompt: str) -> int:
    """Запросить у пользователя целое число.
    При некорректном вводе запрос повторяется."""
    while True:
        value = input(prompt)
        try:
            return int(value)
        except ValueError:
            print("Ошибка: введите целое число.")


def input_non_empty(prompt: str) -> str:
    """Запросить у пользователя непустую строку."""
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("Ошибка: значение не может быть пустым.")
