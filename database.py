import sqlite3


# Create a new SQLite database
conn = sqlite3.connect("task_management.db")
cursor = conn.cursor()

# Create a table for users
cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        email TEXT NOT NULL UNIQUE,
        password_hash TEXT NOT NULL"""
)

# Create a table for tasks
cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS tasks (
        task_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        Task TEXT NOT NULL,
        Description TEXT,
        Priority CHECK (Priority IN ('Low', 'Medium', 'High')) NOT NULL,
        DueDate DATE NOT NULL,
        Status CHECK (Status IN ('Yet to Start', 'In Progress','Completed')) NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users (user_id)
        )"""
)


# CRUD operations


# create user
def create_user(username, email, password_hash):
    cursor.execute(
        "INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)",
        (username, email, password_hash),
    )
    conn.commit()


# create task
def create_task(user_id, task, description, priority, due_date, status):
    cursor.execute(
        "INSERT INTO tasks (user_id, Task, Description, Priority, DueDate, Status) VALUES (?, ?, ?, ?, ?, ?)",
        (user_id, task, description, priority, due_date, status),
    )
    conn.commit()


# update taks
def update_task(
    task_id, task=None, description=None, priority=None, due_date=None, status=None
):
    fields = []
    values = []
    if task:
        fields.append("Task = ?")
        values.append(task)
    if description:
        fields.append("Description = ?")
        values.append(description)
    if priority:
        fields.append("Priority = ?")
        values.append(priority)
    if due_date:
        fields.append("DueDate = ?")
        values.append(due_date)
    if status:
        fields.append("Status = ?")
        values.append(status)
    values.append(task_id)
    cursor.execute(f"UPDATE tasks SET {', '.join(fields)} WHERE task_id = ?", values)
    conn.commit()


# delete task
def delete_task(task_id):
    cursor.execute("DELETE FROM tasks WHERE task_id = ?", (task_id,))
    conn.commit()


# view tasks by user
def get_tasks_by_user(user_id):
    cursor.execute("SELECT * FROM tasks WHERE user_id = ?", (user_id,))
    return cursor.fetchall()


conn.commit()
conn.close()
