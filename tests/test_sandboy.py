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
def big_data(app):
    with app.app_context():
        cloud = Cloud(
                name='private_cloud',
                description='a private cloud')
        db.session.add(cloud)
        for index in range(100):
            db.session.add(Machine(
                hostname=str(index),
                description=str(index),
                cloud=cloud,
                operating_system='Arch 64'))
        db.session.commit() 


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
        json_response = json.loads(response.get_data(as_text=True))
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
        json_response = json.loads(response.get_data(as_text=True))
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

def test_delete(app, data):
    """Can we DELETE an existing resource?"""
    with app.test_client() as client:
        response = client.delete('/cloud/1')
        assert response.status_code == 204

def test_put(app):
    """Do we ignore a POST for an existing resource?"""
    with app.test_client() as client:
        response = client.put('/cloud/1', data=json.dumps({
            'name': 'private_cloud',
            'description': 'a private cloud'
            }))
        assert response.status_code == 201
        json_response = json.loads(response.get_data(as_text=True))
        assert json_response['name'] == 'private_cloud'
        assert json_response['description'] == 'a private cloud'

def test_patch(app, data):
    """Can we patch an existing resource?"""
    with app.test_client() as client:
        response = client.patch('/cloud/1', data=json.dumps({
            'name': 'new cloud',
            'description': 'a private cloud',
            }))
        assert response.status_code == 201
        json_response = json.loads(response.get_data(as_text=True))
        assert json_response['name'] == 'new cloud'
        assert json_response['description'] == 'a private cloud'

def test_put_existing_resource(app, data):
    """Do we update an existing resource on a PUT?"""
    with app.test_client() as client:
        response = client.put('/cloud/1', data=json.dumps({
            'name': 'public_cloud',
            'description': 'my public cloud'
            }))
        assert response.status_code == 201
        json_response = json.loads(response.get_data(as_text=True))
        assert json_response['name'] == 'public_cloud'
        assert json_response['description'] == 'my public cloud'

def test_paginate(app, big_data):
    """Can we properly paginate a get request?"""
    with app.test_client() as client:
        response = client.get('/machine?page=2')
        assert response.status_code == 200
        json_response = json.loads(response.get_data(as_text=True))['resources']
        assert json_response[0]['description'] == '20'

def test_post_missing_field(app):
    """If we leave off a field on a POST, do we get an error?"""
    with app.test_client() as client:
        response = client.post('/cloud', data=json.dumps({
            'description': 'test description'
            }))
        assert response.status_code == 403
        json_response = json.loads(response.get_data())
        assert json_response == {'message': 'cloud.name required'}

def test_post_no_data(app):
    """If we send no JSON data on a POST, do we get an error?"""
    with app.test_client() as client:
        response = client.post('/cloud')
        assert response.status_code == 400
        json_response = json.loads(response.get_data())
        assert json_response == {'message': 'No data received from request'}


