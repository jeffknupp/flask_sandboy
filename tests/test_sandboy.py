"""Tests for sandboy."""
import json

import pytest
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.sandboy import Sandboy

from models import Machine, Cloud, db

@pytest.yield_fixture
def app(request):
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
    app.testing = True
    app.db = db
    db.init_app(app)
    with app.app_context():
        db.create_all()
    sandboy = Sandboy(app, db, [Machine, Cloud])
    yield app

    with app.app_context():
        db.drop_all()
        db.session.remove()


@pytest.fixture
def data(app):
    with app.app_context():
        cloud = Cloud(
                name='private_cloud',
                description='a private cloud')
        db.session.add(cloud)
        db.session.add(Machine(
            hostname='zeus',
            description='application server',
            cloud=cloud,
            operating_system='Arch 64'))
        db.session.add(Machine(
            hostname='apollo',
            description='database server',
            cloud=cloud,
            operating_system='Arch 64'))
        db.session.add(Machine(
            hostname='hermes',
            description='messaging server',
            cloud=cloud,
            operating_system='Ubuntu 13.10 64'))
        db.session.commit()

def test_get_empty_collection(app):
    """Can we get back an appropriate response for an empty collection?"""
    with app.test_client() as client:
        response = client.get('/cloud')
        assert response.status_code == 200

def test_get_single_resource(app, data):
    """Can we successfully get a single resource as JSON?"""
    with app.test_client() as client:
        response = client.get('/machine/1')
        assert response.status_code == 200
        json_response = json.loads(response.get_data()) 
        assert json_response['id'] == 1
        assert json_response['hostname'] == 'zeus'
        assert json_response['description'] == 'application server'
        assert json_response['is_running'] == False
        assert json_response['cloud_id'] == 1

def test_post_resource(app):
    """Can we POST a new resource?"""
    with app.test_client() as client:
        response = client.post('/cloud', data=json.dumps({
            'name': 'temp',
            'description': 'test description'
            }))
        assert response.status_code == 201
        json_response = json.loads(response.get_data()) 
        assert json_response['id'] == 1
        assert json_response['name'] == 'temp'
        assert json_response['description'] == 'test description'

def test_post_existing_resource(app, data):
    """Do we ignore a POST for an existing resource?"""
    with app.test_client() as client:
        response = client.post('/cloud', data=json.dumps({
            'name': 'private_cloud',
            'description': 'a private cloud'
            }))
        assert response.status_code == 204

