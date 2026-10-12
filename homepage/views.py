"""Главная страница, общий каркас страниц и обработчик ошибки 404."""
from django.http import HttpResponse


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
    content = """
    <h1 class="display-4">TeamProject Manager</h1>
    <p class="lead">Система управления командными проектами.</p>
    <p>Основные разделы:</p>
    <a href="/projects/" class="btn btn-primary me-2">Проекты</a>
    <a href="/tasks/" class="btn btn-secondary">Задачи</a>
    """
    return HttpResponse(page("TeamProject Manager", content))


def page_not_found(request, exception):
    """Собственная страница ошибки 404 (подключена через handler404)."""
    content = """
    <h1 class="text-danger">404 – страница не найдена</h1>
    <p>Проверьте адрес или вернитесь на главную.</p>
    <a href="/" class="btn btn-primary">На главную</a>
    """
    return HttpResponse(
        page("404 – страница не найдена", content),
        status=404,
    )
