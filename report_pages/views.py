"""Отчёты: страницы, данные которых получены через Django ORM."""
from datetime import datetime

from django.db.models import Count, F, Max, Min, Q
from django.shortcuts import render

from project_pages.models import Project
from task_pages.models import Task
from team_pages.models import Member

TEMPLATES = "report_pages/"


def projects(request):
    """Проекты и количество задач в каждом (annotate, Count)."""
    # Запрос строится от модели Project, поэтому проекты без задач
    # тоже попадают в результат (аналог LEFT JOIN) со значением 0.
    rows = Project.objects.annotate(
        tasks_count=Count("tasks"),
        open_count=Count("tasks", filter=~Q(tasks__status=Task.STATUS_DONE)),
    ).order_by("-tasks_count", "name")
    context = {"projects": rows}
    return render(request, TEMPLATES + "projects.html", context)


def tasks(request):
    """Незавершённые задачи с проектом и исполнителем."""
    # annotate + F берут поля связанных моделей, values оставляет
    # в результате только нужные ключи (словари).
    rows = (
        Task.objects
        .exclude(status=Task.STATUS_DONE)
        .annotate(
            task_name=F("name"),
            project_name=F("project__name"),
            assignee_name=F("assignee__name"),
        )
        .values(
            "id", "task_name", "status", "due_date",
            "project_name", "assignee_name",
        )
        .order_by(F("due_date").asc(nulls_last=True), "id")
    )
    context = {"tasks": rows}
    return render(request, TEMPLATES + "tasks.html", context)


def deadlines(request):
    """Задачи со сроком не позже даты и участники, свободные в этот день."""
    selected_date = request.GET.get("date", "").strip()
    context = {
        "selected_date": selected_date,
        "tasks": None,
        "free_members": None,
        "error": "",
    }

    if selected_date:
        try:
            day = datetime.strptime(selected_date, "%Y-%m-%d").date()
        except ValueError:
            context["error"] = "Введите дату в формате ГГГГ-ММ-ДД."
        else:
            # Условие due_date__lte само отбрасывает задачи без срока.
            context["tasks"] = (
                Task.objects
                .filter(due_date__lte=day)
                .annotate(
                    task_name=F("name"),
                    assignee_name=F("assignee__name"),
                )
                .values(
                    "id", "task_name", "status", "due_date",
                    "assignee_name",
                )
                .order_by("due_date", "id")
            )
            # Занятые в этот день: невыполненные задачи со сроком day.
            busy_ids = (
                Task.objects
                .filter(due_date=day)
                .exclude(status=Task.STATUS_DONE)
                .values_list("assignee_id", flat=True)
            )
            # Свободные — все остальные участники.
            context["free_members"] = (
                Member.objects
                .exclude(pk__in=busy_ids)
                .order_by("name")
            )
    return render(request, TEMPLATES + "deadlines.html", context)


def workload(request):
    """Участники, у которых не меньше N задач."""
    try:
        minimum = max(int(request.GET.get("min", 1)), 1)
    except ValueError:
        minimum = 1
    # Условие на значение агрегата превращается в SQL-блок HAVING.
    rows = (
        Member.objects
        .annotate(tasks_count=Count("tasks"))
        .filter(tasks_count__gte=minimum)
        .order_by("-tasks_count", "name")
    )
    context = {"members": rows, "minimum": minimum}
    return render(request, TEMPLATES + "workload.html", context)


def stats(request):
    """Общая статистика: итоги, сроки и задачи по статусам."""
    totals = Task.objects.aggregate(
        total=Count("pk"),
        done=Count("pk", filter=Q(status=Task.STATUS_DONE)),
        first_due=Min("due_date"),
        last_due=Max("due_date"),
    )
    by_status = (
        Task.objects
        .values("status")
        .annotate(tasks_count=Count("pk"))
        .order_by("-tasks_count", "status")
    )
    # Три ближайших срока среди невыполненных задач (срез QuerySet).
    nearest = (
        Task.objects
        .select_related("project")
        .exclude(status=Task.STATUS_DONE)
        .exclude(due_date__isnull=True)
        .order_by("due_date", "pk")[:3]
    )
    context = {
        "totals": totals,
        "members_count": Member.objects.count(),
        "by_status": by_status,
        "nearest": nearest,
    }
    return render(request, TEMPLATES + "stats.html", context)
