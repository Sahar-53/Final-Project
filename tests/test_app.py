import pytest
from app import app, db, User, Tasks


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
        db.drop_all()


    # === Create test client === #
    with app.test_client() as client:
        yield client  # allows setup before tests and cleaup after tests

    # === cleans up database after tests
    with app.app_context():
        db.session.remove()
        db.drop_all()  


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
    """Test to check if a user is unable to register with empty username"""

    response = client.post("/register", data={
        "username": "",
        "email": "test-user2@gmail.com",
        "password": "password123"
    }, follow_redirects=True)

    assert b"Username is required" in response.data