import pytest
from app import app, db, Tasks, User


@pytest.fixture
def testuser():
    app.config['Testing'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///memory:"
    app.config['WTF_CRF_ENABLED'] = False

    with app.test_user() as testuser:
        with app.app_context():
            db.create_all()
        yield testuser

        with app.app_context():
            db.drop_all()
