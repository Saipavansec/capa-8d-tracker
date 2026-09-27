-- CAPA / 8D tracker schema (SQLite)

CREATE TABLE IF NOT EXISTS capas (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  title TEXT NOT NULL,
  description TEXT,
  severity TEXT CHECK (severity IN ('low', 'medium', 'high', 'critical')) DEFAULT 'medium',
  status TEXT CHECK (status IN ('open', 'in_progress', 'pending_verification', 'closed')) DEFAULT 'open',
  owner TEXT,
  root_cause_category TEXT,
  created_at TEXT DEFAULT (datetime('now')),
  due_date TEXT,
  closed_at TEXT
);

CREATE TABLE IF NOT EXISTS eight_d_steps (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  capa_id INTEGER NOT NULL REFERENCES capas(id) ON DELETE CASCADE,
  step TEXT NOT NULL,                 -- D0..D8
  content TEXT NOT NULL DEFAULT '',
  completed INTEGER NOT NULL DEFAULT 0,
  completed_at TEXT,
  UNIQUE (capa_id, step)
);

CREATE TABLE IF NOT EXISTS five_whys (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  capa_id INTEGER NOT NULL REFERENCES capas(id) ON DELETE CASCADE,
  level INTEGER NOT NULL,
  question TEXT NOT NULL,
  answer TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS actions (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  capa_id INTEGER NOT NULL REFERENCES capas(id) ON DELETE CASCADE,
  action_type TEXT CHECK (action_type IN ('containment', 'corrective', 'preventive')) NOT NULL,
  description TEXT NOT NULL,
  owner TEXT,
  due_date TEXT,
  done INTEGER NOT NULL DEFAULT 0
);
