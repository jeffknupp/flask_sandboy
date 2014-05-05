"""Tests for sandboy."""

import pytest
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.sandboy import Sandboy

from models import Machine, Cloud, db

@pytest.fixture
def app(request):
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
    app.testing = True
    db.init_app(app)
    with app.app_context():
        db.create_all()
    sandboy = Sandboy(app, db, [Machine, Cloud])
    return app

    def teardown():
        with app.app_context():
            db.drop_all()
            db.seesion.remove()

    request.addfinalizer(teardown)

def test_get_empty_collection(app):
    """Can we get back an appropriate response for an empty collection?"""
    with app.test_client() as client:
        response = client.get('/cloud')
        assert response.status_code == 200
