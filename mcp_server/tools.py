from mcp.server.fastmcp import FastMCP
from mcp_server import db

# Create the MCP server instance — this is the object clients connect to
mcp = FastMCP("Personal Ops - Task Manager")


@mcp.tool()
def add_task(title: str, due_date: str = "") -> dict:
    """
    Add a new task to the task manager.

    Args:
        title: A short description of the task.
        due_date: Optional due date in YYYY-MM-DD format.
    """
    due = due_date if due_date else None
    task_id = db.add_task(title, due)
    return {"success": True, "task_id": task_id, "message": f"Task '{title}' added."}


@mcp.tool()
def list_tasks(status: str = "pending") -> list[dict]:
    """
    List tasks filtered by status.

    Args:
        status: One of 'pending', 'done', or 'all'.
    """
    return db.list_tasks(status)


@mcp.tool()
def complete_task(task_id: int) -> dict:
    """
    Mark a task as completed.

    Args:
        task_id: The numeric id of the task to complete.
    """
    updated = db.complete_task(task_id)
    if updated:
        return {"success": True, "message": f"Task {task_id} marked done."}
    return {"success": False, "message": f"No task found with id {task_id}."}