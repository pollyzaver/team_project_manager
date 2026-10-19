"""Отчёты: страницы, данные которых берутся из SQLite через SQL."""
from datetime import datetime

from django.shortcuts import render

from db.database import fetch_all, fetch_one

TEMPLATES = "report_pages/"


def _no_database(request):
    """Страница-подсказка, если база данных ещё не создана."""
    return render(
        request, TEMPLATES + "no_database.html", status=503,
    )


def projects(request):
    """Проекты и количество задач в каждом (JOIN, COUNT, GROUP BY)."""
    try:
        rows = fetch_all(
            "SELECT projects.id, projects.name, projects.status, "
            "COUNT(tasks.id) AS tasks_count "
            "FROM projects "
            "LEFT JOIN tasks ON tasks.project_id = projects.id "
            "GROUP BY projects.id "
            "ORDER BY tasks_count DESC, projects.name"
        )
    except FileNotFoundError:
        return _no_database(request)
    context = {"projects": rows}
    return render(request, TEMPLATES + "projects.html", context)


def tasks(request):
    """Незавершённые задачи с проектом и исполнителем (JOIN)."""
    try:
        rows = fetch_all(
            "SELECT tasks.id, tasks.name AS task_name, tasks.status, "
            "tasks.due_date, projects.name AS project_name, "
            "members.name AS assignee_name "
            "FROM tasks "
            "JOIN projects ON projects.id = tasks.project_id "
            "JOIN members ON members.id = tasks.assignee_id "
            "WHERE tasks.status <> 'Выполнена' "
            "ORDER BY tasks.due_date IS NULL, tasks.due_date, tasks.id"
        )
    except FileNotFoundError:
        return _no_database(request)
    context = {"tasks": rows}
    return render(request, TEMPLATES + "tasks.html", context)


def deadlines(request):
    """Поиск задач, срок которых наступает не позже выбранной даты."""
    selected_date = request.GET.get("date", "")
    context = {"selected_date": selected_date, "tasks": None, "error": ""}

    if selected_date:
        try:
            datetime.strptime(selected_date, "%Y-%m-%d")
        except ValueError:
            context["error"] = "Введите дату в формате ГГГГ-ММ-ДД."
        else:
            try:
                # Значение передаётся параметром (?), а не склеивается
                # со строкой запроса.
                context["tasks"] = fetch_all(
                    "SELECT tasks.id, tasks.name AS task_name, "
                    "tasks.status, tasks.due_date, "
                    "members.name AS assignee_name "
                    "FROM tasks "
                    "JOIN members ON members.id = tasks.assignee_id "
                    "WHERE tasks.due_date IS NOT NULL "
                    "AND tasks.due_date <= ? "
                    "ORDER BY tasks.due_date",
                    (selected_date,),
                )
            except FileNotFoundError:
                return _no_database(request)
    return render(request, TEMPLATES + "deadlines.html", context)


def workload(request):
    """Участники, у которых не меньше N задач (GROUP BY, HAVING)."""
    try:
        minimum = max(int(request.GET.get("min", 1)), 1)
    except ValueError:
        minimum = 1
    try:
        rows = fetch_all(
            "SELECT members.name, members.role, "
            "COUNT(tasks.id) AS tasks_count "
            "FROM members "
            "JOIN tasks ON tasks.assignee_id = members.id "
            "GROUP BY members.id "
            "HAVING COUNT(tasks.id) >= ? "
            "ORDER BY tasks_count DESC, members.name",
            (minimum,),
        )
    except FileNotFoundError:
        return _no_database(request)
    context = {"members": rows, "minimum": minimum}
    return render(request, TEMPLATES + "workload.html", context)


def stats(request):
    """Общая статистика: итоги и количество задач по статусам."""
    try:
        totals = fetch_one(
            "SELECT COUNT(*) AS total, "
            "COUNT(CASE WHEN status = 'Выполнена' THEN 1 END) AS done "
            "FROM tasks"
        )
        members_count = fetch_one(
            "SELECT COUNT(*) AS members_count FROM members"
        )
        by_status = fetch_all(
            "SELECT status, COUNT(*) AS tasks_count FROM tasks "
            "GROUP BY status ORDER BY tasks_count DESC"
        )
    except FileNotFoundError:
        return _no_database(request)
    context = {
        "totals": totals,
        "members_count": members_count["members_count"],
        "by_status": by_status,
    }
    return render(request, TEMPLATES + "stats.html", context)
