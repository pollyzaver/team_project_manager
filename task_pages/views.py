"""Страницы задач: общий список и карточка задачи."""
from django.shortcuts import render

from storage import load_all
from tasks import find_task_by_id, get_all_tasks


def tasks(request):
    """Список задач всех проектов."""
    context = {
        "tasks": get_all_tasks(load_all()),
    }
    return render(request, "task_pages/task_list.html", context)


def task_detail(request, task_id):
    """Карточка задачи: исполнитель, срок, статус и проект."""
    projects_list = load_all()
    task = find_task_by_id(get_all_tasks(projects_list), task_id)

    project = None
    if task is not None:
        project = next(p for p in projects_list if task in p.tasks)

    context = {
        "task": task,
        "project": project,
    }
    return render(
        request,
        "task_pages/task_detail.html",
        context,
        status=404 if task is None else 200,
    )
