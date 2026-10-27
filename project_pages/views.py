"""Страницы проектов: список с поиском и карточка проекта (Django ORM)."""
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, render

from project_pages.models import Project
from task_pages.models import Task

# Допустимые варианты сортировки: значение параметра sort из адреса
# сопоставляется с полем модели, а не подставляется в order_by() как есть.
SORT_FIELDS = {
    "name": "name",
    "manager": "manager",
    "start": "start_date",
    "tasks": "-tasks_count",
}
SORT_OPTIONS = [
    ("name", "названию"),
    ("manager", "руководителю"),
    ("start", "дате начала"),
    ("tasks", "числу задач"),
]


def projects(request):
    """Список проектов: поиск, фильтр по статусу и сортировка."""
    query = request.GET.get("q", "").strip()
    status = request.GET.get("status", "").strip()
    sort = request.GET.get("sort", "name")
    if sort not in SORT_FIELDS:
        sort = "name"

    # annotate(Count) добавляет каждому проекту число его задач.
    projects_list = Project.objects.annotate(tasks_count=Count("tasks"))

    # Поиск по нескольким полям сразу (условие ИЛИ через Q).
    if query:
        projects_list = projects_list.filter(
            Q(name__icontains=query)
            | Q(description__icontains=query)
            | Q(manager__icontains=query)
        )

    # Фильтр по статусу: принимаем только известные значения.
    if status in dict(Project.STATUS_CHOICES):
        projects_list = projects_list.filter(status=status)
    else:
        status = ""

    projects_list = projects_list.order_by(SORT_FIELDS[sort], "pk")

    context = {
        "projects": projects_list,
        "query": query,
        "selected_status": status,
        "statuses": Project.STATUS_CHOICES,
        "sort": sort,
        "sort_options": SORT_OPTIONS,
    }
    return render(request, "project_pages/project_list.html", context)


def project_detail(request, project_id):
    """Карточка проекта: данные, команда, задачи и прогресс."""
    # select_related подгружает команду одним запросом с проектом,
    # prefetch_related — задачи и участников отдельными запросами.
    project = get_object_or_404(
        Project.objects
        .select_related("team")
        .prefetch_related("tasks", "team__members"),
        pk=project_id,
    )

    # Сводные показатели одним запросом: всего задач и выполненных.
    totals = project.tasks.aggregate(
        total=Count("pk"),
        done=Count("pk", filter=Q(status=Task.STATUS_DONE)),
    )
    progress = 0
    if totals["total"]:
        progress = int(totals["done"] / totals["total"] * 100)

    context = {
        "project": project,
        "tasks_total": totals["total"],
        "progress": progress,
    }
    return render(request, "project_pages/project_detail.html", context)
