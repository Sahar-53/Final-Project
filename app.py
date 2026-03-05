from flask import Flask, render_template, url_for
import sqlite3

conn = sqlite3.connect("task_management.db")
cursor = conn.cursor()


app = Flask(__name__)


# ---- Home page ----#
@app.route("/")
def index():
    return render_template("home.html")


# ---- Login page ----#
@app.route("/login")
def login():
    return render_template("login.html")


# ---- Sign-up page ----#
@app.route("/register")
def register():
    return render_template("register.html")


@app.route("/dashboard")
def dahsboard():
    return render_template("dashboard.html")


# CRUD operations


# ----View Tasks by User----#
@app.route("/tasks")
def get_tasks_by_user(user_id):
    cursor.execute("SELECT * FROM tasks WHERE user_id = ?", (user_id,))
    return cursor.fetchall()


# ----Create Task----#
@app.route("/tasks/create")
def create_task(user_id, task, description, priority, due_date, status):
    cursor.execute(
        "INSERT INTO tasks (user_id, Task, Description, Priority, DueDate, Status) VALUES (?, ?, ?, ?, ?, ?)",
        (user_id, task, description, priority, due_date, status),
    )
    conn.commit()


# ----Update Task----#
@app.route("/tasks/update")
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


# ----Delete Task----#
@app.route("/tasks/delete")
def delete_task(task_id):
    cursor.execute("DELETE FROM tasks WHERE task_id = ?", (task_id,))
    conn.commit()


if __name__ == "__main__":
    app.run(debug=True)
