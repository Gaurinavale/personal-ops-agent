import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "tasks.db"


def get_connection():
    """Open a connection to the SQLite database."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # lets us access columns by name
    return conn


def init_db():
    """Create the tasks table if it doesn't already exist."""
    conn = get_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            due_date TEXT,
            status TEXT NOT NULL DEFAULT 'pending'
        )
    """)
    conn.commit()
    conn.close()


def add_task(title: str, due_date: str | None = None) -> int:
    """Insert a new task, return its id."""
    conn = get_connection()
    cursor = conn.execute(
        "INSERT INTO tasks (title, due_date, status) VALUES (?, ?, 'pending')",
        (title, due_date),
    )
    conn.commit()
    task_id = cursor.lastrowid
    conn.close()
    return task_id


def list_tasks(status: str = "pending") -> list[dict]:
    """Return all tasks matching a status ('pending', 'done', or 'all')."""
    conn = get_connection()
    if status == "all":
        rows = conn.execute("SELECT * FROM tasks").fetchall()
    else:
        rows = conn.execute(
            "SELECT * FROM tasks WHERE status = ?", (status,)
        ).fetchall()
    conn.close()
    return [dict(row) for row in rows]


def complete_task(task_id: int) -> bool:
    """Mark a task as done. Returns True if a row was updated."""
    conn = get_connection()
    cursor = conn.execute(
        "UPDATE tasks SET status = 'done' WHERE id = ?", (task_id,)
    )
    conn.commit()
    updated = cursor.rowcount > 0
    conn.close()
    return updated