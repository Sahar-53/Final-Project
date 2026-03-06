from flask import Flask, render_template, url_for, redirect, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import (UserMixin, LoginManager, login_user, logout_user, login_required, current_user)
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, ValidationError
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import or_, CheckConstraint
from datetime import date

# ---------Initialize the Flask app------------#
app = Flask(__name__)

# Configure SQLite database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///task_management.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False  # Avoids a warning
app.config["SECRET_KEY"] = "This is a secret key"  # to secure a session cookie

# For security purposes
app.config["SESSION_COOKIE_SECURE"] = True
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
app.config['PREFERRED_URL_SCHEME'] = 'https'


# Create database instance
db = SQLAlchemy(app)

# This part allows the app and Flask-Login to work together
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


# Load user for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# ----------Create User database structure----------#
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)


# ----------Create Registration form with valdidators-----------#
class RegisterForm(FlaskForm):

    username = StringField(
        "Username",
        validators=[
            DataRequired(),
            Length(min=4, max=20),
        ],
    )

    email = StringField(
        "Email",
        validators=[
            DataRequired(),
            Email(),
        ],
    )

    password = PasswordField(
        "Password",
        validators=[
            DataRequired(),
            Length(min=6, max=20),
        ],
    )

    submit = SubmitField("Register")

    # -------------Check for unique values--------------#
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


# ---------------Create Login form---------------#
class LoginForm(FlaskForm):

    username = StringField(
        "Username or Email",
        validators=[
            DataRequired(),
        ],
    )

    password = PasswordField(
        "Password",
        validators=[
            DataRequired(message="Password is required"),
        ],
    )

    submit = SubmitField("Login")


# ------------------Tasks table--------------------#
class Tasks(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500))
    due_date = db.Column(db.Date, nullable=False)
    status = db.Column(
        db.String(20),
        CheckConstraint("status IN ('To Do', 'In Progress', 'Completed')"),
        nullable=False,
    )
    priority = db.Column(
        db.String(20),
        CheckConstraint("priority IN ('Low', 'Medium', 'High')"),
        nullable=False,
    )


# --------------- Home page -------------#
@app.route("/")
def index():
    return render_template("home.html")


# ---------------- Login page --------------#
@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()  # To add the form

    # ------Authentication-----------#
    if form.validate_on_submit():
        user_input = form.username.data  # this is whatever the user typed

        # ----- checks for username and email address---------#
        user = User.query.filter(
            or_(User.username == user_input, User.email == user_input)
        ).first()

        # ------ checks if password matches with the one on database----#
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for("tasks"))
        else:
            return render_template(
                "login.html", form=form, error="Invalid username or password"
            )

    return render_template(
        "login.html", form=form
    )  # form variable created to pass the form to HTML template


# ---- Sign-up page -------#
@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()

    # -----Password hash feature-----------#
    if form.validate_on_submit():

        hashed_password = generate_password_hash(form.password.data)

        new_user = User(
            username=form.username.data, email=form.email.data, password=hashed_password
        )

        # -----Add to database ----------#
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for("login"))

    print(form.errors)  # To print form validation errors

    return render_template("register.html", form=form)


# ============Tasks Dashboard---------------#
@app.route("/tasks", methods=["GET", "POST"])
@login_required  # ---user can only access if logged in
# ------ This sends all user tasks to the dashboard page.
def tasks():

    tasks = Tasks.query.filter_by(user_id=current_user.id).all()

    status_query = request.args.get('status')

    if status_query:
        tasks = Tasks.query.filter_by(status=status_query).all()
    else:
        tasks = Tasks.query.all()

    return render_template("tasks.html", tasks=tasks)


# ---------------CRUD operations-----------#


# -----------Create new task-------------#
@app.route("/tasks/new", methods=["GET", "POST"])
@login_required
def create_task():

    if request.method == "POST":

        title = request.form["title"]
        description = request.form["description"]
        priority = request.form["priority"]
        due_date = request.form["due_date"]
        status = request.form["status"]

        # convert string to Python date
        due_date = date.fromisoformat(request.form["due_date"])

        task = Tasks(
            title=title,
            description=description,
            priority=priority,
            due_date=due_date,
            status=status,
            user_id=current_user.id,
        )

        db.session.add(task)
        db.session.commit()

        flash("Task created successfully")

        return redirect(url_for("tasks"))

    return render_template("create_task.html")


# -----------Edit a task-------------#
@app.route("/tasks/<int:id>/edit", methods=["GET", "POST"])
def edit_task(id):
    task_to_edit = Tasks.query.get_or_404(id)

    if request.method == "POST":
        task_to_edit.title = request.form["title"]
        task_to_edit.description = request.form["description"]
        task_to_edit.priority = request.form["priority"]
        task_to_edit.due_date = request.form["due_date"]
        task_to_edit.status = request.form["status"]

        task_to_edit.due_date = date.fromisoformat(request.form["due_date"])

        db.session.commit()

        return redirect(url_for("tasks"))

    return render_template("edit_task.html", task=task_to_edit)


# -----------Delete a task-------------#
@app.route("/tasks/<int:id>/delete")
def delete_task(id):
    task = Tasks.query.get_or_404(id)

    db.session.delete(task)
    db.session.commit()

    return redirect(url_for("tasks"))


# ----------Logout route---------#
@app.route("/logout", methods=["GET", "POST"])
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))


if __name__ == "__main__":
    with app.app_context():  # Needed for DB operations
        db.create_all()  # Creates the database and tables
    app.run(debug=True)
