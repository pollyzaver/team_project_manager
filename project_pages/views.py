"""Страницы проектов: список и карточка проекта."""
from django.shortcuts import render

from projects import find_project_by_id
from storage import load_all
from tasks import calculate_progress


def projects(request):
    """Список всех проектов из data/projects.json."""
    context = {
        "projects": load_all(),
    }
    return render(request, "project_pages/project_list.html", context)


def project_detail(request, project_id):
    """Карточка проекта: данные, команда, задачи и прогресс."""
    projects_list = load_all()
    project = find_project_by_id(projects_list, project_id)

    context = {
        "project": project,
    }
    if project is not None:
        context["progress"] = int(calculate_progress(project.tasks))

    return render(
        request,
        "project_pages/project_detail.html",
        context,
        status=404 if project is None else 200,
    )
