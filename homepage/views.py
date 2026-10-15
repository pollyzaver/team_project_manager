"""Главная страница, общий каркас страниц и обработчик ошибки 404."""
from django.shortcuts import render


def page(title, content):
    """Собрать HTML-страницу: общий каркас, навигация и содержимое.

    title — заголовок вкладки браузера, content — HTML-код,
    который view-функция вставляет внутрь <main>.
    """
    bootstrap = (
        "https://cdn.jsdelivr.net/npm/bootstrap@5.3.3"
        "/dist/css/bootstrap.min.css"
    )
    return f"""<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{title}</title>
    <link rel="stylesheet" href="{bootstrap}">
</head>
<body>
    <nav class="nav">
        <a class="nav-link" href="/">Главная</a>
        <a class="nav-link" href="/projects/">Проекты</a>
        <a class="nav-link" href="/tasks/">Задачи</a>
    </nav>
    <main class="container">{content}</main>
</body>
</html>"""


def index(request):
    """Главная страница с описанием системы и ссылками на разделы."""
    return render(request, "homepage/index.html")


def page_not_found(request, exception):
    """Собственная страница ошибки 404 (подключена через handler404)."""
    return render(request, "404.html", status=404)
