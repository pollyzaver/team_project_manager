# main.py
# Система управления командными проектами

from datetime import date

# Данные проекта
project_name = "Разработка мобильного приложения"
project_description = "Создание приложения для доставки еды"
project_status = "Активен"
start_date = date(2026, 9, 1)
end_date = date(2026, 12, 15)
project_manager = "Анна Петрова"

# Данные участников
member_1_name = "Иван Иванов"
member_1_role = "Разработчик"
member_2_name = "Мария Смирнова"
member_2_role = "Дизайнер"
member_3_name = "Петр Сидоров"
member_3_role = "Тестировщик"

# Данные задач
task_1_name = "Дизайн интерфейса"
task_1_status = "Выполнена"
task_2_name = "Разработка бэкенда"
task_2_status = "В работе"
task_3_name = "Настройка сервера"
task_3_status = "Новая"

# Функция определения статуса задачи
def get_task_status_text(status):
    if status == "Выполнена":
        return "Завершено"
    elif status == "В работе":
        return "В процессе"
    elif status == "Новая":
        return "Ожидает начала"
    else:
        return "Статус не определен"

# Функция проверки активности проекта
def is_project_active(status):
    if status == "Активен":
        return True
    else:
        return False

# Подсчет выполненных задач
completed_tasks = 0
total_tasks = 3

if task_1_status == "Выполнена":
    completed_tasks = completed_tasks + 1
if task_2_status == "Выполнена":
    completed_tasks = completed_tasks + 1
if task_3_status == "Выполнена":
    completed_tasks = completed_tasks + 1

# Вычисление прогресса
progress = (float(completed_tasks) / float(total_tasks)) * 100

# Вывод информации
print("СИСТЕМА УПРАВЛЕНИЯ КОМАНДНЫМИ ПРОЕКТАМИ")
print("")

print("Информация о проекте:")
print("Название: " + project_name)
print("Описание: " + project_description)
print("Руководитель: " + project_manager)
print("Дата начала: " + start_date.strftime("%d.%m.%Y"))
print("Дата окончания: " + end_date.strftime("%d.%m.%Y"))

if is_project_active(project_status):
    print("Статус: Активен")
else:
    print("Статус: Не активен")

print("")

print("Участники команды:")
print("1. " + member_1_name + " - " + member_1_role)
print("2. " + member_2_name + " - " + member_2_role)
print("3. " + member_3_name + " - " + member_3_role)

print("")

print("Задачи проекта:")
print("1. " + task_1_name + " - " + get_task_status_text(task_1_status))
print("2. " + task_2_name + " - " + get_task_status_text(task_2_status))
print("3. " + task_3_name + " - " + get_task_status_text(task_3_status))

print("")

print("Прогресс проекта: " + str(int(progress)) + "%")
print("Выполнено задач: " + str(completed_tasks) + " из " + str(total_tasks))

print("")
print("Конец отчета")