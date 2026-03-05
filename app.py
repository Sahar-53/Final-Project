from flask import Flask, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, ValidationError, EqualTo


"""
import sqlite3

conn = sqlite3.connect("task_management.db")
cursor = conn.cursor()
"""

app = Flask(__name__)


# Configure SQLite database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///task_management.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False  # Avoids a warning
app.config["SECRET_KEY"] = "This is a secret key"  # to secure a session cookie

# Create database instance
db = SQLAlchemy(app)


# Create User database structure
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)


# Create Registration form with valdidators
class RegisterForm(FlaskForm):

    username = StringField(
        "Username",
        validators=[
            DataRequired(message="Username is required"),
            Length(
                min=4, max=20, message="Username must be between 4 and 20 characters"
            ),
        ],
    )

    email = StringField(
        "Email",
        validators=[
            DataRequired(message="Email is required"),
            Email(message="Enter a valid email address"),
        ],
    )

    password = PasswordField(
        "Password",
        validators=[
            DataRequired(),
            Length(min=6, max=20, message="Password must be at least 6 characters"),
        ],
    )

    confirm_password = PasswordField(
        "Confirm Password",
        validators=[
            DataRequired(),
            EqualTo("password", message="Passwords must match"),
        ],
    )

    submit = SubmitField("Register")


# Check for unique values
def validate_username(self, username):
    existing_user_username = User.query.filter_by(username=username.data).first()

    if existing_user_username:
        raise ValidationError(
            "That username already exists. Please choose a different one."
        )


def validate_email(self, email):
    existing_user_email = User.query.filter_by(email=email.data).first()

    if existing_user_email:
        raise ValidationError(
            "That email address already exists. Please choose a different one."
        )


# Create Login form
class LoginForm(FlaskForm):

    identifier = StringField(
        "Username or Email",
        validators=[
            DataRequired(message="Username or Email is required"),
        ],
    )

    password = PasswordField(
        "Password",
        validators=[
            DataRequired(message="Password is required"),
        ],
    )

    submit = SubmitField("Login")


# ---- Home page ----#
@app.route("/")
def index():
    return render_template("home.html")


# ---- Login page ----#
@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()  # To add the form
    return render_template(
        "login.html", form=form
    )  # form variable created to pass the form to HTML template


# ---- Sign-up page ----#
@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    return render_template("register.html", form=form)


@app.route("/dashboard")
def dahsboard():
    return render_template("dashboard.html")


# CRUD operations

"""
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

"""

if __name__ == "__main__":
    with app.app_context():  # Needed for DB operations
        db.create_all()  # Creates the database and tables
    app.run(debug=True)
