<<<<<<< HEAD
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

conn.commit()
conn.close()
=======
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

conn.commit()
conn.close()
>>>>>>> b7300f7fed2f396191f3e221b616b504455fcacd
