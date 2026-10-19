-- ==========================================
-- TeamProject Manager: SQL-запросы проекта
-- Знак ? — место для значения, которое передаёт Python.
-- ==========================================

-- 1. Список проектов (выборка списка)
SELECT id, name, manager, status
FROM projects
ORDER BY name;

-- 2. Список участников с ролями (выборка списка)
SELECT id, name, role
FROM members
ORDER BY name;

-- 3. Активные проекты (WHERE)
SELECT id, name, start_date, end_date
FROM projects
WHERE status = 'Активен';

-- 4. Незавершённые задачи (WHERE)
SELECT id, name, status, due_date
FROM tasks
WHERE status <> 'Выполнена'
ORDER BY due_date IS NULL, due_date, id;

-- 5. Задачи со сроком не позже выбранной даты (WHERE, параметр)
SELECT id, name, status, due_date
FROM tasks
WHERE due_date IS NOT NULL AND due_date <= ?
ORDER BY due_date;

-- 6. Задачи с проектом и исполнителем (JOIN трёх таблиц)
SELECT tasks.id, tasks.name AS task_name, tasks.status, tasks.due_date,
       projects.name AS project_name, members.name AS assignee_name
FROM tasks
JOIN projects ON projects.id = tasks.project_id
JOIN members ON members.id = tasks.assignee_id
WHERE tasks.status <> 'Выполнена'
ORDER BY tasks.due_date IS NULL, tasks.due_date, tasks.id;

-- 7. Команда проекта с участниками (JOIN)
SELECT teams.name AS team_name, members.name AS member_name, members.role
FROM teams
JOIN members ON members.team_id = teams.id
WHERE teams.project_id = ?
ORDER BY members.name;

-- 8. Общее число задач и число выполненных (COUNT)
SELECT COUNT(*) AS total,
       COUNT(CASE WHEN status = 'Выполнена' THEN 1 END) AS done
FROM tasks;

-- 9. Число участников всех команд (COUNT)
SELECT COUNT(*) AS members_count
FROM members;

-- 10. Проекты и количество задач (LEFT JOIN, COUNT, GROUP BY)
SELECT projects.id, projects.name, projects.status,
       COUNT(tasks.id) AS tasks_count
FROM projects
LEFT JOIN tasks ON tasks.project_id = projects.id
GROUP BY projects.id
ORDER BY tasks_count DESC, projects.name;

-- 11. Количество задач по статусам (COUNT, GROUP BY)
SELECT status, COUNT(*) AS tasks_count
FROM tasks
GROUP BY status
ORDER BY tasks_count DESC;

-- 12. Нагрузка участников: у кого не меньше N задач (GROUP BY, HAVING)
SELECT members.name, members.role, COUNT(tasks.id) AS tasks_count
FROM members
JOIN tasks ON tasks.assignee_id = members.id
GROUP BY members.id
HAVING COUNT(tasks.id) >= ?
ORDER BY tasks_count DESC, members.name;

-- 13. Ближайшие сроки задач (сортировка, LIMIT)
SELECT name, due_date
FROM tasks
WHERE due_date IS NOT NULL
ORDER BY due_date
LIMIT 3;
