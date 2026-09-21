"""Точка запуска приложения «Система управления командными проектами»."""
from projects import add_member, find_member
from tasks import (
    add_task,
    calculate_progress,
    count_completed_tasks,
)
from storage import (
    load_project_data,
    load_tasks,
    save_project_data,
    save_tasks,
)
from utils import input_non_empty

PROJECTS_FILE = "data/projects.json"
TASKS_FILE = "data/tasks.json"


def show_project(project, members) -> None:
    """Вывести информацию о проекте и участниках команды."""
    print("Информация о проекте:")
    print(project.get_info_text())
    status_text = "Активен" if project.is_active() else "Не активен"
    print(f"Статус: {status_text}")
    print()
    print("Участники команды:")
    for index, member in enumerate(members, start=1):
        print(f"{index}. {member}")


def show_tasks(tasks) -> None:
    """Вывести список задач проекта."""
    print("Задачи проекта:")
    for index, task in enumerate(tasks, start=1):
        print(f"{index}. {task}")


def show_progress(tasks) -> None:
    """Вывести прогресс выполнения проекта."""
    progress = calculate_progress(tasks)
    completed = count_completed_tasks(tasks)
    print(f"Прогресс проекта: {int(progress)}%")
    print(f"Выполнено задач: {completed} из {len(tasks)}")


def add_new_task(tasks, members) -> None:
    """Запросить данные новой задачи у пользователя и добавить её."""
    name = input_non_empty("Название задачи: ")
    assignee_name = input_non_empty("Ответственный (имя участника): ")
    found = find_member(members, assignee_name)
    if not found:
        print("Участник с таким именем не найден.")
        return
    add_task(tasks, name, "Новая", found[0])
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
    project, members = load_project_data(PROJECTS_FILE)
    tasks = load_tasks(TASKS_FILE, members)

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
            add_new_task(tasks, members)
        elif choice == "0":
            save_project_data(PROJECTS_FILE, project, members)
            save_tasks(TASKS_FILE, tasks)
            print("Данные сохранены. До свидания!")
            break
        else:
            print("Неверный выбор, попробуйте снова.")


if __name__ == "__main__":
    main()