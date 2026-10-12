"""Страницы задач: общий список и карточка задачи."""
from django.http import HttpResponse
from django.utils.html import escape

from homepage.views import page
from storage import load_all
from tasks import find_task_by_id, get_all_tasks

STATUS_BADGES = {
    "Выполнена": "bg-success",
    "В работе": "bg-primary",
    "Новая": "bg-secondary",
}


def tasks(request):
    """Список задач всех проектов."""
    items = ""
    for project in load_all():
        for task in project.tasks:
            badge = STATUS_BADGES.get(task.status, "bg-dark")
            items += f"""
        <li class="list-group-item d-flex justify-content-between">
            <a href="/tasks/{task.id}/">{escape(task.name)}</a>
            <span class="badge {badge}">{escape(task.status)}</span>
        </li>
        """
    content = f"""
    <h1>Задачи</h1>
    <ul class="list-group">{items}</ul>
    """
    return HttpResponse(page("TeamProject – задачи", content))


def task_detail(request, task_id):
    """Карточка задачи: исполнитель, срок, статус и проект."""
    projects_list = load_all()
    task = find_task_by_id(get_all_tasks(projects_list), task_id)

    if task is None:
        content = """
        <h1 class="text-danger">Задача не найдена</h1>
        <a href="/tasks/" class="btn btn-outline-secondary">
            ← к списку задач
        </a>
        """
        return HttpResponse(
            page("Задача не найдена", content),
            status=404,
        )

    project = next(p for p in projects_list if task in p.tasks)
    badge = STATUS_BADGES.get(task.status, "bg-dark")
    due_date = escape(task.due_date) if task.due_date else "не задан"

    content = f"""
    <div class="card">
        <div class="card-body">
            <h5 class="card-title">{escape(task.name)}</h5>
            <p class="card-text">
                <strong>ID:</strong> {task.id}
            </p>
            <p class="card-text">
                <strong>Проект:</strong>
                <a href="/projects/{project.id}/">
                    {escape(project.name)}
                </a>
            </p>
            <p class="card-text">
                <strong>Исполнитель:</strong> {escape(task.assignee.name)}
            </p>
            <p class="card-text">
                <strong>Срок:</strong> {due_date}
            </p>
            <p class="card-text">
                Статус: <span class="badge {badge}">
                    {escape(task.status)}
                </span>
                ({task.get_status_text()})
            </p>
            <a href="/tasks/" class="btn btn-outline-secondary">
                ← к списку задач
            </a>
        </div>
    </div>
    """
    return HttpResponse(page(task.name, content), status=200)
