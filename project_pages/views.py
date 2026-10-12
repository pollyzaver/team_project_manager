"""Страницы проектов: список и карточка проекта."""
from django.http import HttpResponse
from django.utils.html import escape

from homepage.views import page
from projects import find_project_by_id
from storage import load_all
from tasks import calculate_progress


def projects(request):
    """Список всех проектов из data/projects.json."""
    items = ""
    for project in load_all():
        status = "активен" if project.is_active() else "не активен"
        badge = "bg-success" if project.is_active() else "bg-secondary"
        items += f"""
        <li class="list-group-item d-flex justify-content-between">
            <a href="/projects/{project.id}/">{escape(project.name)}</a>
            <span class="badge {badge}">{status}</span>
        </li>
        """
    content = f"""
    <h1>Проекты</h1>
    <ul class="list-group">{items}</ul>
    """
    return HttpResponse(page("TeamProject – проекты", content))


def project_detail(request, project_id):
    """Карточка проекта: данные, команда, задачи и прогресс."""
    projects_list = load_all()
    project = find_project_by_id(projects_list, project_id)

    if project is None:
        content = """
        <h1 class="text-danger">Проект не найден</h1>
        <a href="/projects/" class="btn btn-outline-secondary">
            ← к списку проектов
        </a>
        """
        return HttpResponse(
            page("Проект не найден", content),
            status=404,
        )

    status = "активен" if project.is_active() else "не активен"
    badge = "bg-success" if project.is_active() else "bg-secondary"
    progress = int(calculate_progress(project.tasks))

    members = ""
    for member in project.team.members:
        members += (
            f'<li class="list-group-item">{escape(member.name)} – '
            f"{escape(member.role)}</li>"
        )
    tasks_items = ""
    for task in project.tasks:
        tasks_items += (
            '<li class="list-group-item">'
            f'<a href="/tasks/{task.id}/">{escape(task.name)}</a> '
            f"– {escape(task.status)}</li>"
        )

    content = f"""
    <div class="card mb-3">
        <div class="card-body">
            <h5 class="card-title">{escape(project.name)}</h5>
            <p class="card-text">
                <strong>ID:</strong> {project.id}
            </p>
            <p class="card-text">{escape(project.description)}</p>
            <p class="card-text">
                <strong>Руководитель:</strong> {escape(project.manager)}
            </p>
            <p class="card-text">
                <strong>Сроки:</strong>
                {escape(project.start_date)} – {escape(project.end_date)}
            </p>
            <p class="card-text">
                Статус: <span class="badge {badge}">{status}</span>
            </p>
            <p class="card-text">
                <strong>Прогресс:</strong> {progress}%
                ({len(project.tasks)} задач)
            </p>
            <a href="/projects/" class="btn btn-outline-secondary">
                ← к списку проектов
            </a>
        </div>
    </div>
    <h2>Команда: {escape(project.team.name)}</h2>
    <ul class="list-group mb-3">{members}</ul>
    <h2>Задачи</h2>
    <ul class="list-group">{tasks_items}</ul>
    """
    return HttpResponse(page(project.name, content), status=200)
