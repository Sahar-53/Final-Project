import pytest
from app import app, db, User, Tasks, RegisterForm, LoginForm


@pytest.fixture
def client():

    # === Configure for testing === #
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",  # temporary database used
        "WTF_CSRF_ENABLED": False  # disable CRF protecting for testing
    })

    # === Create database tables === #
    with app.app_context():
        db.create_all()

    # === Create test client === #
    with app.test_client() as client:
        yield client  # allows setup before tests and cleaup after tests


# ======== Tests ======== #
# ===== Test 1 - Regisatration ===== #
def test_registeration_user(client):
    """Test to check if a user is able to register with correct details"""

    response = client.post("/register", data={
        "username": "testuser",
        "email": "test-user@gmail.com",
        "password": "password123"
    }, follow_redirects=True)  # redirect to avoid 302 status code

    assert response.status_code == 200  # checks that the repsonse status is 200 (success)


# ===== Test 2 - Registration ===== #
def test_regiseration_invalid(client):
    """Test to check if a user is unable to register with not unique email address"""

    with app.app_context():
        form = RegisterForm(data={
            "username": "Testuser2",
            "email": "test-user@gmail.com",
            "password": "password123"
        }, follow_redirects=True)

        assert form.validate() is False
        assert "That email address already exists. Please choose a different one." in form.email.errors


# ===== Test 3 - Login ===== #
def test_login_invalid(client):
    """Test to check if a user is unable to login with incorrect details"""

    with client.application.app_context():
        user = User(username="testuser", password="password123")
        db.session.add(user)
        db.session.commit

    response = client.post("/login", data={
        "username": "testuser",
        "password": "wrongpassword"
    }, follow_redirects=True)

    assert response.status_code == 200
    user = User.query.filter_by(password="wrongpassword").first()
    assert user is None


# ===== Test 4 - Login ===== #
def test_login_valid(client):
    """Test to check if a user is unable to login with incorrect details"""

    with client.application.app_context():
        user = User(username="testuser", password="password123")
        db.session.add(user)
        db.session.commit

    response = client.post("/login", data={
        "username": "testuser",
        "password": "password123"
    }, follow_redirects=True)

    assert response.status_code == 200
    user = User.query.filter_by(username="testuser").first()
    assert user is not None