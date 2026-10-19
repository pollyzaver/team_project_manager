-- ==========================================
-- TeamProject Manager: структура базы данных
-- ==========================================

-- Проекты
CREATE TABLE IF NOT EXISTS projects (
  id INTEGER PRIMARY KEY,
  name TEXT NOT NULL,
  description TEXT,
  manager TEXT,
  start_date TEXT,
  end_date TEXT,
  status TEXT NOT NULL
);

-- Команды: у каждого проекта одна команда
CREATE TABLE IF NOT EXISTS teams (
  id INTEGER PRIMARY KEY,
  name TEXT NOT NULL,
  project_id INTEGER NOT NULL UNIQUE,
  FOREIGN KEY (project_id) REFERENCES projects (id)
);

-- Участники команд
CREATE TABLE IF NOT EXISTS members (
  id INTEGER PRIMARY KEY,
  name TEXT NOT NULL,
  role TEXT,
  team_id INTEGER NOT NULL,
  FOREIGN KEY (team_id) REFERENCES teams (id)
);

-- Задачи: относятся к проекту и назначены участнику
CREATE TABLE IF NOT EXISTS tasks (
  id INTEGER PRIMARY KEY,
  name TEXT NOT NULL,
  status TEXT NOT NULL,
  due_date TEXT,
  project_id INTEGER NOT NULL,
  assignee_id INTEGER NOT NULL,
  FOREIGN KEY (project_id) REFERENCES projects (id),
  FOREIGN KEY (assignee_id) REFERENCES members (id)
);
