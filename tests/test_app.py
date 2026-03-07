import pytest
from app import app, db


@pytest.fixture
def client():
    app.config['Testing'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///memory:"  # temporary database used
    app.config['WTF_CRF_ENABLED'] = False  # disable CRF protecting for testing

    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client  # allows setup before tests and cleaup after tests

        with app.app_context():
            db.drop_all()  # deletes the test records


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
    }, follow_redirects=True)  # redirect to avoid 302 status code

    assert b"Username is required" in response.data