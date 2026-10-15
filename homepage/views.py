"""Главная страница и обработчик ошибки 404."""
from django.shortcuts import render


def index(request):
    """Главная страница с описанием системы и ссылками на разделы."""
    return render(request, "homepage/index.html")


def page_not_found(request, exception):
    """Собственная страница ошибки 404 (подключена через handler404)."""
    return render(request, "404.html", status=404)
