"""Точка запуска приложения «Система управления командными проектами»."""
from projects import add_member, create_project, find_member
from tasks import (
    add_task,
    calculate_progress,
    count_completed_tasks,
    delete_task,
    filter_tasks_by_status,
    sort_tasks_by_due_date,
    update_task_status,
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


def show_project(project) -> None:
    """Вывести информацию о проекте, команде и участниках."""
    print("Информация о проекте:")
    print(project.get_info_text())
    status_text = "Активен" if project.is_active() else "Не активен"
    print(f"Статус: {status_text}")
    print()
    print("Участники команды:")
    for index, member in enumerate(project.team.members, start=1):
        print(f"{index}. {member}")


def show_tasks(tasks) -> None:
    """Вывести список задач."""
    if not tasks:
        print("Задач пока нет.")
        return
    print("Задачи:")
    for index, task in enumerate(tasks, start=1):
        print(f"{index}. {task}")


def show_progress(tasks) -> None:
    """Вывести прогресс выполнения проекта."""
    progress = calculate_progress(tasks)
    completed = count_completed_tasks(tasks)
    print(f"Прогресс проекта: {int(progress)}%")
    print(f"Выполнено задач: {completed} из {len(tasks)}")


def add_new_task(project) -> None:
    """Запросить данные новой задачи у пользователя и добавить её."""
    name = input_non_empty("Название задачи: ")
    assignee_name = input_non_empty("Ответственный (имя участника): ")
    found = find_member(project.team.members, assignee_name)
    if not found:
        print("Участник с таким именем не найден.")
        return
    due_date = input(
        "Срок выполнения (ДД.ММ.ГГГГ, можно оставить пустым): "
    ).strip()
    add_task(project.tasks, name, "Новая", found[0], due_date)
    print("Задача добавлена.")


def change_task_status(tasks) -> None:
    """Запросить у пользователя задачу и новый статус, обновить его."""
    name = input_non_empty("Название задачи: ")
    new_status = input_non_empty(
        "Новый статус (Новая/В работе/Выполнена): "
    )
    if update_task_status(tasks, name, new_status):
        print("Статус обновлён.")
    else:
        print("Задача не найдена.")


def remove_task(tasks) -> None:
    """Запросить название задачи у пользователя и удалить её."""
    name = input_non_empty("Название задачи для удаления: ")
    if delete_task(tasks, name):
        print("Задача удалена.")
    else:
        print("Задача не найдена.")


def add_new_member(project) -> None:
    """Запросить данные нового участника и добавить его в команду."""
    name = input_non_empty("Имя участника: ")
    role = input_non_empty("Роль участника: ")
    add_member(project.team.members, name, role)
    print("Участник добавлен в команду.")


def show_tasks_by_status(tasks) -> None:
    """Запросить статус у пользователя и вывести только такие задачи."""
    status = input_non_empty(
        "Статус для фильтра (Новая/В работе/Выполнена): "
    )
    show_tasks(filter_tasks_by_status(tasks, status))


def show_tasks_sorted_by_due_date(tasks) -> None:
    """Вывести задачи, отсортированные по сроку выполнения."""
    show_tasks(sort_tasks_by_due_date(tasks))


def create_new_project(projects) -> None:
    """Запросить данные нового проекта у пользователя и добавить его."""
    name = input_non_empty("Название проекта: ")
    description = input_non_empty("Описание: ")
    manager = input_non_empty("Руководитель: ")
    start_date = input_non_empty("Дата начала (ДД.ММ.ГГГГ): ")
    end_date = input_non_empty("Дата окончания (ДД.ММ.ГГГГ): ")
    team_name = input_non_empty("Название команды: ")
    create_project(
        projects, name, description, manager, start_date, end_date,
        team_name,
    )
    print("Проект создан.")


def print_project_list(projects) -> None:
    """Вывести список всех проектов с номерами."""
    if not projects:
        print("Проектов пока нет.")
        return
    print("Список проектов:")
    for index, project in enumerate(projects, start=1):
        print(f"{index}. {project}")


def choose_project(projects):
    """Запросить у пользователя номер проекта и вернуть его объект.

    Возвращает None, если проектов нет, введён "0" или введено
    некорректное значение.
    """
    print_project_list(projects)
    if not projects:
        return None
    choice = input_non_empty("Номер проекта (0 — назад): ")
    if choice == "0":
        return None
    try:
        index = int(choice) - 1
    except ValueError:
        print("Нужно ввести число.")
        return None
    if 0 <= index < len(projects):
        return projects[index]
    print("Проекта с таким номером нет.")
    return None


def print_project_menu() -> None:
    """Вывести меню действий внутри выбранного проекта."""
    print()
    print("1. Показать информацию о проекте")
    print("2. Показать задачи")
    print("3. Показать прогресс проекта")
    print("4. Добавить задачу")
    print("5. Изменить статус задачи")
    print("6. Удалить задачу")
    print("7. Добавить участника в команду")
    print("8. Показать задачи по статусу")
    print("9. Показать задачи по сроку выполнения")
    print("0. Вернуться к списку проектов")


def project_menu(project) -> None:
    """Цикл меню действий внутри одного выбранного проекта."""
    while True:
        print_project_menu()
        choice = input("Выберите действие: ").strip()

        if choice == "1":
            show_project(project)
        elif choice == "2":
            show_tasks(project.tasks)
        elif choice == "3":
            show_progress(project.tasks)
        elif choice == "4":
            add_new_task(project)
        elif choice == "5":
            change_task_status(project.tasks)
        elif choice == "6":
            remove_task(project.tasks)
        elif choice == "7":
            add_new_member(project)
        elif choice == "8":
            show_tasks_by_status(project.tasks)
        elif choice == "9":
            show_tasks_sorted_by_due_date(project.tasks)
        elif choice == "0":
            break
        else:
            print("Неверный выбор, попробуйте снова.")


def print_main_menu() -> None:
    """Вывести главное меню приложения."""
    print()
    print("1. Выбрать проект")
    print("2. Создать новый проект")
    print("0. Сохранить и выйти")


def main() -> None:
    """Загрузить данные и запустить меню приложения."""
    projects = load_project_data(PROJECTS_FILE)
    load_tasks(TASKS_FILE, projects)

    print("СИСТЕМА УПРАВЛЕНИЯ КОМАНДНЫМИ ПРОЕКТАМИ")

    while True:
        print_main_menu()
        choice = input("Выберите действие: ").strip()

        if choice == "1":
            project = choose_project(projects)
            if project is not None:
                project_menu(project)
        elif choice == "2":
            create_new_project(projects)
        elif choice == "0":
            save_project_data(PROJECTS_FILE, projects)
            save_tasks(TASKS_FILE, projects)
            print("Данные сохранены. До свидания!")
            break
        else:
            print("Неверный выбор, попробуйте снова.")


if __name__ == "__main__":
    main()
