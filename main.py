"""Точка запуска приложения «Система управления командными проектами»."""
from projects import get_project_info_text, is_project_active
from tasks import (
    get_task_status_text,
    count_completed_tasks,
    calculate_progress,
    add_task,
)
from storage import load_data, save_data
from utils import input_non_empty

PROJECTS_FILE = "data/projects.json"
TASKS_FILE = "data/tasks.json"


def show_project(project: dict, members: list) -> None:
    """Вывести информацию о проекте и участниках команды."""
    print("Информация о проекте:")
    print(get_project_info_text(project))
    status_text = "Активен" if is_project_active(project) else "Не активен"
    print(f"Статус: {status_text}")
    print()
    print("Участники команды:")
    for index, member in enumerate(members, start=1):
        print(f"{index}. {member['name']} - {member['role']}")


def show_tasks(tasks: list) -> None:
    """Вывести список задач проекта."""
    print("Задачи проекта:")
    for index, task in enumerate(tasks, start=1):
        status_text = get_task_status_text(task["status"])
        print(f"{index}. {task['name']} - {status_text}")


def show_progress(tasks: list) -> None:
    """Вывести прогресс выполнения проекта."""
    progress = calculate_progress(tasks)
    completed = count_completed_tasks(tasks)
    print(f"Прогресс проекта: {int(progress)}%")
    print(f"Выполнено задач: {completed} из {len(tasks)}")


def add_new_task(tasks: list) -> None:
    """Запросить данные новой задачи у пользователя и добавить её."""
    name = input_non_empty("Название задачи: ")
    assignee = input_non_empty("Ответственный: ")
    add_task(tasks, name, "Новая", assignee)
    print("Задача добавлена.")


def print_menu() -> None:
    """Вывести меню приложения."""
    print()
    print("1. Показать информацию о проекте")
    print("2. Показать задачи")
    print("3. Показать прогресс проекта")
    print("4. Добавить задачу")
    print("0. Сохранить и выйти")


def main() -> None:
    """Загрузить данные и запустить меню приложения."""
    default_project_data = {"project": {}, "members": []}
    project_data = load_data(PROJECTS_FILE, default_project_data)
    tasks = load_data(TASKS_FILE, [])

    project = project_data["project"]
    members = project_data["members"]

    print("СИСТЕМА УПРАВЛЕНИЯ КОМАНДНЫМИ ПРОЕКТАМИ")

    while True:
        print_menu()
        choice = input("Выберите действие: ").strip()

        if choice == "1":
            show_project(project, members)
        elif choice == "2":
            show_tasks(tasks)
        elif choice == "3":
            show_progress(tasks)
        elif choice == "4":
            add_new_task(tasks)
        elif choice == "0":
            save_data(PROJECTS_FILE, project_data)
            save_data(TASKS_FILE, tasks)
            print("Данные сохранены. До свидания!")
            break
        else:
            print("Неверный выбор, попробуйте снова.")


if __name__ == "__main__":
    main()