# TeamProject Manager

## Назначение
Приложение для управления командными проектами. Позволяет создавать проекты, назначать команды, ставить задачи и отслеживать их выполнение. Доступно в двух видах: консольное меню (ПР3) и веб-интерфейс на Django (ПР5, ПР6); данные для страниц отчётов берутся из базы SQLite (ПР7); начиная с ПР9 веб-страницы получают данные через Django ORM из базы `db.sqlite3`.

## Целевая аудитория
Руководители команд, тимлиды, участники проектных групп, желающие структурировать работу над проектами.

## Описание предметной области
Управление проектами (Project Management). Основные процессы: создание проекта, формирование команды, постановка и распределение задач, контроль статуса выполнения.

## Основные классы

### Project
Проект, которым управляет команда.
- **Атрибуты**: `id` (уникальный числовой идентификатор, используется в адресах страниц), `name`, `description`, `manager`, `start_date`, `end_date`, `status`, `team` (объект `Team`, назначенный на проект), `tasks` (список задач `Task`, относящихся к проекту).
- **Методы**: `is_active()` — проверка активности проекта; `get_info_text()` — текстовое описание проекта, включая название команды; `__str__()` — краткое строковое представление (название и статус).

### Team
Команда, назначенная на проект.
- **Атрибуты**: `name`, `members` (список объектов `Member`).
- **Методы**: `add_member()` — добавить участника напрямую в команду; `find_member()` — поиск участников по подстроке имени; `__str__()` — строковое представление («Название команды (N участников)»).

### Member
Участник команды проекта.
- **Атрибуты**: `name`, `role`.
- **Методы**: `__str__()` — строковое представление участника («Имя - Роль»).

### Task
Задача проекта.
- **Атрибуты**: `id` (уникальный числовой идентификатор), `name`, `status`, `assignee` (объект `Member`, ответственный за задачу), `due_date` (срок выполнения, необязательный).
- **Методы**: `is_completed()` — проверка выполнения задачи; `get_status_text()` — статус в читаемом виде; `__str__()` — строковое представление задачи.

## Взаимодействие объектов
Объект `Task` хранит прямую ссылку на объект `Member` в атрибуте `assignee` (а не просто имя строкой) — можно обращаться к данным участника через задачу, например `task.assignee.name`. Объект `Project` хранит прямую ссылку на объект `Team` в атрибуте `team`, а команда, в свою очередь, хранит список `Member`. Список задач проекта (`Project.tasks`) — тоже прямая часть объекта проекта, а не отдельная коллекция, передаваемая по приложению вручную.

## Основные функции
- Создание нового проекта (`create_project`), поиск проектов по названию (`find_project`) и по идентификатору (`find_project_by_id`).
- Добавление участников в команду проекта (`add_member`).
- Поиск участников по имени (`find_member`).
- Создание и назначение задач по проекту (`add_task`), включая срок выполнения.
- Изменение статуса задачи (`update_task_status`) и удаление задачи (`delete_task`).
- Отображение списка проектов с их статусами.
- Просмотр списка задач по проекту, фильтрация по статусу (`filter_tasks_by_status`) и сортировка по статусу/сроку выполнения (`sort_tasks_by_status`, `sort_tasks_by_due_date`).
- Расчёт прогресса выполнения проекта (`calculate_progress`).
- Сбор задач всех проектов (`get_all_tasks`) и поиск задачи по идентификатору (`find_task_by_id`) — используются веб-страницами.

## Структура проекта
- `manage.py` — точка входа Django (проверка конфигурации, запуск сервера);
- `teamproject/` — конфигурационный пакет Django-проекта (`settings.py`, корневой `urls.py`, `wsgi.py`, `asgi.py`);
- `homepage/`, `project_pages/`, `task_pages/` — Django-приложения (главная, страницы проектов, страницы задач); у каждого есть своя папка `templates/<приложение>/`; в `project_pages/models.py` и `task_pages/models.py` лежат модели Django ORM `Project` и `Task` (ПР9);
- `team_pages/` — приложение с моделями `Team` и `Member` (ПР9), страниц у него нет;
- `templates/` — общие шаблоны проекта: `base.html`, `404.html`, `includes/navigation.html`;
- `homepage/static/homepage/` — статические файлы: `css/style.css`, `js/main.js`, `img/logo.png`;
- `main.py` — точка запуска, двухуровневое меню приложения (список/создание проектов снаружи, действия внутри выбранного проекта);
- `models/` — пакет с классами предметной области:
  - `project.py` — класс `Project`;
  - `team.py` — класс `Team`;
  - `member.py` — класс `Member`;
  - `task.py` — класс `Task`;
- `projects.py` — функции работы с проектами, командами и участниками (`create_project`, `find_project`, `find_project_by_id`, `next_project_id`, `add_member`, `find_member`);
- `tasks.py` — функции работы с коллекцией задач (`add_task`, `delete_task`, `update_task_status`, `count_completed_tasks`, `calculate_progress`, `filter_tasks_by_status`, `sort_tasks_by_status`, `sort_tasks_by_due_date`, `get_all_tasks`, `find_task_by_id`);
- `storage.py` — загрузка и сохранение объектов в JSON (`load_all` загружает проекты вместе с задачами одним вызовом);
- `utils.py` — вспомогательные функции безопасного ввода;
- `db/` — работа с SQLite: `database.py` (соединение, `fetch_all`, `fetch_one`, создание таблиц), `import_json.py` (перенос данных из JSON в базу ПР7), `inspect_source_db.py` (просмотр структуры базы ПР7) и `import_sqlite_to_orm.py` (перенос данных из базы ПР7 в таблицы Django ORM, ПР9);
- `sql/` — SQL-файлы: `schema.sql` (создание таблиц) и `queries.sql` (запросы проекта);
- `report_pages/` — Django-приложение «Отчёты»: страницы, данные которых получены SQL-запросами к SQLite;
- `data/` — файлы данных (`projects.json` — список проектов с их командами, `tasks.json` — задачи, сгруппированные по названию проекта, `teamproject.sqlite` — исходная база ПР7, создаётся командой импорта и в Git не хранится);
- `db.sqlite3` — база данных Django (ПР9), создаётся командой `migrate`, в Git не хранится;
- `tests/` — автоматизированные тесты.

## Формат хранения данных
Данные хранятся в формате JSON: `data/projects.json` — список проектов, у каждого вложена его команда с участниками; `data/tasks.json` — словарь вида `{"Название проекта": [задачи...]}`. У проектов и задач есть поле `id`; если в старом файле его нет, при загрузке оно назначается автоматически (следующее свободное число), а при сохранении записывается в файл. При загрузке JSON преобразуется в объекты `Project`/`Team`/`Member`/`Task`; при сохранении объекты преобразуются обратно (связь `Task.assignee` сохраняется как имя участника, задачи привязываются к проекту по его названию).

## Требования
- Python 3.x
- Django 5.2
- pytest
- flake8

Установка зависимостей:

pip install -r requirements.txt


## Запуск программы

Консольная версия (ПР3):

python main.py

Веб-версия (ПР5), команды выполняются из корня проекта:

python manage.py check

python manage.py runserver

После запуска сайт доступен по адресу http://127.0.0.1:8000/

База данных для раздела «Отчёты» (ПР7) создаётся и заполняется из JSON одной командой:

python -m db.import_json

Команду можно запускать повторно — таблицы очищаются и заполняются заново.

База данных Django (ПР9): после клонирования применяются миграции и переносятся данные из базы ПР7:

python manage.py migrate

python -m db.import_json

python -m db.import_sqlite_to_orm

Перенос можно запускать повторно: записи ищутся по `id` и обновляются, дубликаты не создаются.


## Запуск тестов

pytest


## Проверка качества кода

flake8


## Веб-интерфейс на Django (ПР5)
Консольное приложение сохранено, рядом с ним добавлен Django-проект. Веб-слой использует готовые классы и JSON-хранилище ПР3: view-функции загружают данные через `storage.load_all()`, находят объекты по `id` (`find_project_by_id`, `find_task_by_id`) и формируют HTML-страницы.

### Django-проект и приложения
- `teamproject/` — конфигурационный пакет: `settings.py` (настройки, `INSTALLED_APPS`, `DEBUG`, `ALLOWED_HOSTS`, локализация `ru-RU`, `Europe/Moscow`), `urls.py` (корневые маршруты и `handler404`);
- `homepage` — главная страница и страница ошибки 404 (общий каркас вынесен в `templates/base.html`);
- `project_pages` — список проектов и страница проекта;
- `task_pages` — список задач и страница задачи.

Отдельное приложение для участников и команд не создавалось: они показываются на странице проекта. Приложения названы `project_pages` и `task_pages`, потому что имена `projects` и `tasks` уже заняты модулями `projects.py` и `tasks.py` консольной части.

### Страницы и URL
| URL | View-функция | Что показывает |
|---|---|---|
| `/` | `homepage.views.index` | главная страница, ссылки на разделы |
| `/projects/` | `project_pages.views.projects` | список проектов со статусами |
| `/projects/<id>/` | `project_pages.views.project_detail` | карточка проекта: данные, прогресс, команда, задачи |
| `/tasks/` | `task_pages.views.tasks` | список задач всех проектов |
| `/tasks/<id>/` | `task_pages.views.task_detail` | карточка задачи: проект, исполнитель, срок, статус |
| любой другой | `homepage.views.page_not_found` | страница ошибки 404 |

Если проект или задача с указанным `id` не найдены, view возвращает страницу с HTTP-статусом 404.

### HTML, CSS и Bootstrap
Каркас всех страниц (кодировка, `viewport`, Bootstrap 5.3 через CDN, шапка с логотипом, навигация, подвал) находится в `templates/base.html`. Оформление — классы Bootstrap (`container`, `card`, `list-group`, `badge`, `btn`) и собственный `style.css`. Автоэкранирование данных выполняет шаблонизатор Django.

### Шаблоны Django (ПР6)
HTML больше не формируется в Python: view-функции собирают словарь контекста и вызывают `render(request, "шаблон.html", context)`.
- **Наследование.** `base.html` задаёт блоки `title` и `content`; страницы подключаются через `{% extends "base.html" %}` и переопределяют блоки.
- **Включаемые шаблоны (`{% include %}`).** `includes/navigation.html` (меню; активный раздел определяется по `request.resolver_match.namespace`), `project_card.html`, `project_status.html`, `task_status.html`.
- **Теги.** `{% for %}…{% empty %}` (списки проектов, задач, участников), `{% if %}/{% elif %}/{% else %}` (статусы, «не найдено»), `{% with %}`, `{% url %}`, `{% load static %}`/`{% static %}`.
- **Фильтры.** `length` (количество проектов и задач), `default` (пустые значения), `truncatewords` (краткое описание в карточке).
- **Именованные URL и пространства имён** (`app_name` в `urls.py` приложений): `homepage:index`, `projects:list`, `projects:detail`, `tasks:list`, `tasks:detail`. Ссылки строятся через `{% url 'projects:detail' project.id %}`, поэтому не зависят от адресов.
- **Шаблоны ошибок.** Для несуществующего проекта или задачи возвращается тот же шаблон страницы со статусом 404; `handler404` использует `templates/404.html` (виден при `DEBUG = False`, при `DEBUG = True` Django показывает свою техническую страницу).
- **Статика.** `STATIC_URL = "static/"`, файлы лежат в `homepage/static/homepage/` и подключаются через `{% static %}`; `TEMPLATES["DIRS"]` указывает на общую папку `templates/`.

### Текущее состояние
Консольное приложение, тесты и JSON-хранилище ПР3 работают без изменений. Веб-интерфейс пока только читает данные: ORM, формы и изменение данных появятся позже.

## База данных SQLite и SQL (ПР7)
Данные проекта перенесены из JSON в реляционную базу SQLite. Консольное приложение, JSON-хранилище и веб-страницы ПР5–ПР6 работают как раньше (JSON остаётся предыдущей реализацией); новый раздел «Отчёты» получает данные из SQLite. Django ORM пока не используется — только SQL и стандартный модуль `sqlite3`.

### Структура базы данных
| Таблица | Поля | Связи |
|---|---|---|
| `projects` | `id` (PK), `name`, `description`, `manager`, `start_date`, `end_date`, `status` | — |
| `teams` | `id` (PK), `name`, `project_id` | `project_id` → `projects.id` (у проекта одна команда) |
| `members` | `id` (PK), `name`, `role`, `team_id` | `team_id` → `teams.id` |
| `tasks` | `id` (PK), `name`, `status`, `due_date`, `project_id`, `assignee_id` | `project_id` → `projects.id`, `assignee_id` → `members.id` |

Даты хранятся как текст `ГГГГ-ММ-ДД` (при импорте переводятся из `ДД.ММ.ГГГГ`), чтобы их можно было сравнивать и сортировать в SQL; отсутствующий срок задачи — `NULL`. Внешние ключи проверяются, потому что для каждого соединения выполняется `PRAGMA foreign_keys = ON`.

### Файлы
- `sql/schema.sql` — создание таблиц (`CREATE TABLE IF NOT EXISTS`);
- `sql/queries.sql` — 20 запросов проекта: списки, `WHERE` (`IN`, `BETWEEN`, `LIKE`, `IS NULL`), `JOIN`, `COUNT`, `GROUP BY`, `HAVING`, `LIMIT/OFFSET`, `DISTINCT`, подзапрос;
- `db/database.py` — `get_connection()` (включает `sqlite3.Row`, чтобы обращаться к полям по именам), `init_db()`, `fetch_all()`, `fetch_one()`;
- `db/import_json.py` — читает данные через `storage.load_all()` и добавляет их в таблицы через `executemany()`.

### Страницы раздела «Отчёты»
| URL | View | Запрос |
|---|---|---|
| `/reports/` | `report_pages.views.stats` | `COUNT`, `GROUP BY` по статусам |
| `/reports/projects/` | `projects` | `LEFT JOIN` + `COUNT` + `GROUP BY`: проекты и число задач |
| `/reports/tasks/` | `tasks` | `JOIN` трёх таблиц: незавершённые задачи с проектом и исполнителем |
| `/reports/deadlines/?date=ГГГГ-ММ-ДД` | `deadlines` | задачи со сроком не позже даты и участники, свободные в этот день |
| `/reports/workload/?min=N` | `workload` | `GROUP BY` + `HAVING`: участники, у которых не меньше N задач |

Значения из адресной строки передаются в запросы параметрами (`?`), а не подставляются в текст запроса. Путь данных: SQLite → SQL → `sqlite3` → view → context → шаблон → страница. Если базы ещё нет, страницы показывают подсказку выполнить `python -m db.import_json`.

### Текущее состояние
После ПР9 все веб-страницы получают данные через Django ORM; файлы SQL-слоя (`sql/`, `db/database.py`, `db/import_json.py`) остаются в проекте как предыдущая реализация и источник данных для переноса.

## Django ORM (ПР9)
Слой данных веб-части переведён с `sqlite3` и JSON на Django ORM: таблицы описаны моделями, структурой базы управляют миграции, view-функции получают объекты через менеджер `objects`. Адреса, шаблоны и пользовательские сценарии ПР5–ПР7 сохранены. Консольное приложение (`main.py`) и JSON-хранилище работают как раньше.

Путь данных: `view → Django ORM → SQL → SQLite (db.sqlite3) → объекты моделей → context → шаблон → HTML`.

### Модели и связи
| Модель (приложение) | Поля | Связи |
|---|---|---|
| `Project` (`project_pages`) | `name`, `description`, `manager`, `start_date`, `end_date`, `status` | — |
| `Team` (`team_pages`) | `name` | `project` — `OneToOneField` на `Project`, `related_name="team"`, `CASCADE` |
| `Member` (`team_pages`) | `name`, `role` | `team` — `ForeignKey` на `Team`, `related_name="members"`, `CASCADE` |
| `Task` (`task_pages`) | `name`, `status`, `due_date` | `project` — `ForeignKey` на `Project`, `related_name="tasks"`, `PROTECT`; `assignee` — `ForeignKey` на `Member`, `related_name="tasks"`, `PROTECT` |

- Первичный ключ `id` Django создаёт сам (`BigAutoField`).
- Даты — `DateField`; срок задачи и даты проекта необязательны (`null=True, blank=True`).
- Статус проекта и задачи ограничен списком `choices`.
- `PROTECT` у задач запрещает удалять проект или участника, пока на них ссылаются задачи: история работы не теряется. Команда удаляется вместе с проектом, участник — вместе с командой (`CASCADE`).
- Методы моделей: `Project.is_active()`, `Task.is_completed()`, `Task.get_status_text()`, `Task.complete()`.
- Все модели зарегистрированы в админ-панели (`/admin/`, нужен `python manage.py createsuperuser`).

### Стратегия перехода и перенос данных
Выбран вариант 2: Django создаёт собственные таблицы в `db.sqlite3` (настройка `DATABASES` не менялась), а база ПР7 `data/teamproject.sqlite` остаётся нетронутым источником. Скрипт `db/import_sqlite_to_orm.py` читает её через `sqlite3` и создаёт записи через ORM (`update_or_create` по `id`, одна транзакция `transaction.atomic()`). Порядок: проекты → команды → участники → задачи. Даты переводятся из `ГГГГ-ММ-ДД` в `date`. `db/inspect_source_db.py` выводит структуру и число записей исходной базы (только чтение).

### Миграции
Файлы `0001_initial.py` лежат в `project_pages/migrations/`, `team_pages/migrations/`, `task_pages/migrations/` и хранятся в Git.

python manage.py makemigrations

python manage.py showmigrations

python manage.py sqlmigrate task_pages 0001

python manage.py migrate

`makemigrations` только создаёт файлы с описанием изменений, `migrate` применяет их к базе и создаёт таблицы.

### Страницы и запросы ORM
| Страница | Что делает | Приёмы ORM |
|---|---|---|
| `/projects/?q=&status=&sort=` | поиск, фильтр по статусу, сортировка | `annotate(Count)`, `filter(Q(...) \| Q(...))`, `icontains`, `order_by` по словарю допустимых полей |
| `/projects/<id>/` | карточка проекта, прогресс | `get_object_or_404`, `select_related("team")`, `prefetch_related`, `aggregate(Count, filter=Q)` |
| `/tasks/?q=&project=&assignee=&status=&date=&sort=&page=` | список задач | `select_related`, `filter` по нескольким условиям и по внешним ключам, `Q` по полям связанных моделей, `due_date__lte`, `order_by(F().asc(nulls_last=True))`, `Paginator`, `{% querystring %}` |
| `/tasks/<id>/` | карточка задачи | `get_object_or_404`, `select_related("project", "assignee")` |
| `/reports/` | итоги и статусы | `aggregate(Count, Min, Max)`, `values().annotate(Count)`, `exclude()`, срез `[:3]` |
| `/reports/projects/` | проекты и число задач | `annotate(Count)` от `Project` (проекты без задач остаются со значением 0), условный `Count(filter=~Q())` |
| `/reports/tasks/` | незавершённые задачи | `exclude`, `annotate(F("project__name"))`, `values` |
| `/reports/deadlines/?date=` | задачи до даты, свободные участники | `filter(due_date__lte)`, `values_list(flat=True)`, `exclude(pk__in=...)` |
| `/reports/workload/?min=N` | нагрузка участников | `annotate(Count)` + `filter(tasks_count__gte)` (SQL `HAVING`) |

Значения из адреса проверяются: некорректная дата, номер страницы или фильтр не вызывают ошибку, неизвестное значение `sort` заменяется сортировкой по умолчанию. Для несуществующего `id` возвращается 404. Поле сортировки выбирается из словаря допустимых вариантов, а не подставляется в `order_by()` как есть. Поиск `icontains` в SQLite не различает регистр только для латиницы, для кириллицы регистр учитывается.

### Операции в Django shell
python manage.py shell

from project_pages.models import Project
from team_pages.models import Member, Team
from task_pages.models import Task

project = Project.objects.create(name="Тест", manager="Я")
team = Team.objects.create(name="Тест-команда", project=project)
member = Member.objects.create(name="Тестер", role="QA", team=team)
task = Task.objects.create(name="Задача", project=project, assignee=member)
task.status = "Выполнена"
task.save()
Task.objects.get(pk=task.pk).status
project.tasks.all()
task.delete()

### Проверка
python manage.py check

python manage.py makemigrations --check

python manage.py showmigrations

pytest -v

flake8 . --extend-exclude=venv

## План развития проекта
На следующих этапах планируется:
- привязка задач к проекту по `id` проекта вместо названия;
- связь «многие-ко-многим» между `Team` и `Member` (участник — в нескольких командах);
- формы создания и изменения проектов, команд и задач через веб-интерфейс;
- реализация аутентификации пользователей;
- разработка REST API для управления сущностями;
- контейнеризация приложения с помощью Docker;
- настройка CI/CD.
