"""SQLite persistence for the CAPA / 8D tracker."""

from __future__ import annotations

import json
import sqlite3
from pathlib import Path

SCHEMA_PATH = Path(__file__).resolve().parent.parent / "schema.sql"


def get_connection(db_path="capa.db"):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db(db_path="capa.db"):
    conn = get_connection(db_path)
    conn.executescript(SCHEMA_PATH.read_text())
    conn.commit()
    return conn


def create_capa(conn, title, description="", severity="medium",
                owner=None, due_date=None, root_cause_category=None):
    cur = conn.execute(
        """INSERT INTO capas (title, description, severity, owner, due_date,
                              root_cause_category)
           VALUES (?, ?, ?, ?, ?, ?)""",
        (title, description, severity, owner, due_date, root_cause_category))
    conn.commit()
    return cur.lastrowid


def list_capas(conn, status=None):
    if status:
        rows = conn.execute("SELECT * FROM capas WHERE status = ? ORDER BY id",
                            (status,)).fetchall()
    else:
        rows = conn.execute("SELECT * FROM capas ORDER BY id").fetchall()
    return [dict(r) for r in rows]


def set_step(conn, capa_id, step, content):
    """Save 8D step content (dict or str); content dicts are stored as JSON."""
    payload = json.dumps(content) if isinstance(content, dict) else content
    conn.execute(
        """INSERT INTO eight_d_steps (capa_id, step, content)
           VALUES (?, ?, ?)
           ON CONFLICT (capa_id, step)
           DO UPDATE SET content = excluded.content""",
        (capa_id, step, payload))
    conn.commit()


def complete_step(conn, capa_id, step):
    from datetime import datetime, timezone
    conn.execute(
        """INSERT INTO eight_d_steps (capa_id, step, completed, completed_at)
           VALUES (?, ?, 1, ?)
           ON CONFLICT (capa_id, step)
           DO UPDATE SET completed = 1, completed_at = excluded.completed_at""",
        (capa_id, step, datetime.now(timezone.utc).isoformat()))
    conn.commit()


def add_five_why(conn, capa_id, level, question, answer):
    conn.execute(
        "INSERT INTO five_whys (capa_id, level, question, answer) VALUES (?, ?, ?, ?)",
        (capa_id, level, question, answer))
    conn.commit()


def add_action(conn, capa_id, action_type, description, owner=None, due_date=None):
    conn.execute(
        """INSERT INTO actions (capa_id, action_type, description, owner, due_date)
           VALUES (?, ?, ?, ?, ?)""",
        (capa_id, action_type, description, owner, due_date))
    conn.commit()


def capa_progress(conn, capa_id):
    """Return 0-100 progress based on completed D0..D8 steps."""
    from .eight_d import STEPS
    rows = conn.execute(
        "SELECT step FROM eight_d_steps WHERE capa_id = ? AND completed = 1",
        (capa_id,)).fetchall()
    done = {r["step"] for r in rows}
    total = len(STEPS)
    return round(100 * sum(1 for code, _, _ in STEPS if code in done) / total, 1)


def overdue_capas(conn):
    rows = conn.execute(
        """SELECT * FROM capas
           WHERE status != 'closed' AND due_date IS NOT NULL
             AND date(due_date) < date('now')
           ORDER BY due_date""").fetchall()
    return [dict(r) for r in rows]


def pareto_root_causes(conn):
    """Count closed/in-progress CAPAs by root-cause category (Pareto input)."""
    rows = conn.execute(
        """SELECT COALESCE(root_cause_category, 'Uncategorized') AS category,
                  COUNT(*) AS n
           FROM capas GROUP BY category ORDER BY n DESC""").fetchall()
    return [(r["category"], r["n"]) for r in rows]
