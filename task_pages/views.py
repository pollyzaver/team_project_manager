"""Страницы задач: список с фильтрами и карточка задачи (Django ORM)."""
from datetime import datetime

from django.core.paginator import Paginator
from django.db.models import F, Q
from django.shortcuts import get_object_or_404, render

from project_pages.models import Project
from task_pages.models import Task
from team_pages.models import Member

PER_PAGE = 5

# Допустимые поля сортировки. Пользователь выбирает ключ, а в order_by()
# попадает только значение из этого словаря. Задачи без срока при
# сортировке по сроку уходят в конец списка.
SORT_FIELDS = {
    "due": F("due_date").asc(nulls_last=True),
    "name": "name",
    "project": "project__name",
    "assignee": "assignee__name",
    "status": "status",
}
SORT_OPTIONS = [
    ("due", "сроку"),
    ("name", "названию"),
    ("project", "проекту"),
    ("assignee", "исполнителю"),
    ("status", "статусу"),
]


def _to_int(value):
    """Вернуть целое число из строки или None, если это не число."""
    if value.isascii() and value.isdigit():
        return int(value)
    return None


def tasks(request):
    """Список задач: поиск, фильтры, сортировка и постраничный вывод."""
    query = request.GET.get("q", "").strip()
    project_id = request.GET.get("project", "").strip()
    assignee_id = request.GET.get("assignee", "").strip()
    status = request.GET.get("status", "").strip()
    due_date = request.GET.get("date", "").strip()
    sort = request.GET.get("sort", "due")
    if sort not in SORT_FIELDS:
        sort = "due"
    error = None

    # select_related подгружает проект и исполнителя тем же запросом,
    # поэтому шаблон не делает отдельный запрос на каждую задачу.
    tasks_list = Task.objects.select_related("project", "assignee")

    # Поиск по названию задачи, проекта или имени исполнителя.
    if query:
        tasks_list = tasks_list.filter(
            Q(name__icontains=query)
            | Q(project__name__icontains=query)
            | Q(assignee__name__icontains=query)
        )

    # Фильтры по проекту и исполнителю (по внешним ключам).
    if _to_int(project_id) is not None:
        tasks_list = tasks_list.filter(project_id=int(project_id))
    if _to_int(assignee_id) is not None:
        tasks_list = tasks_list.filter(assignee_id=int(assignee_id))

    # Фильтр по статусу: принимаем только известные значения.
    if status in dict(Task.STATUS_CHOICES):
        tasks_list = tasks_list.filter(status=status)
    else:
        status = ""

    # Фильтр «срок не позже даты»; задачи без срока в него не входят.
    if due_date:
        try:
            selected_date = datetime.strptime(due_date, "%Y-%m-%d").date()
        except ValueError:
            error = "Укажите корректную дату."
        else:
            tasks_list = tasks_list.filter(due_date__lte=selected_date)

    # Сортировка, а при равных значениях — по идентификатору.
    tasks_list = tasks_list.order_by(SORT_FIELDS[sort], "pk")

    # Пагинация применяется после фильтров и сортировки.
    paginator = Paginator(tasks_list, PER_PAGE)
    page_obj = paginator.get_page(request.GET.get("page"))

    context = {
        "tasks": page_obj,
        "page_obj": page_obj,
        "query": query,
        "selected_project": project_id,
        "selected_assignee": assignee_id,
        "selected_status": status,
        "due_date": due_date,
        "sort": sort,
        "sort_options": SORT_OPTIONS,
        "projects": Project.objects.order_by("name"),
        "members": Member.objects.order_by("name"),
        "statuses": Task.STATUS_CHOICES,
        "error": error,
    }
    return render(request, "task_pages/task_list.html", context)


def task_detail(request, task_id):
    """Карточка задачи: исполнитель, срок, статус и проект."""
    task = get_object_or_404(
        Task.objects.select_related("project", "assignee"),
        pk=task_id,
    )
    context = {
        "task": task,
        "project": task.project,
    }
    return render(request, "task_pages/task_detail.html", context)
