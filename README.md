# Flask-Sandboy

[![Build Status](https://travis-ci.org/jeffknupp/flask_sandboy.svg?branch=develop)](https://travis-ci.org/jeffknupp/flask_sandboy)
[![Coverage Status](https://coveralls.io/repos/jeffknupp/flask_sandboy/badge.png)](https://coveralls.io/r/jeffknupp/flask_sandboy)
[![Downloads](https://img.shields.io/pypi/dm/flask_sandboy.svg)](https://pypi.python.org/pypi/flask_sandboy/)
[![Latest Version](https://img.shields.io/pypi/v/flask_sandboy.svg)](https://pypi.python.org/pypi/flask_sandboy/)

Flask-Sandboy is [sandman's](http://www.github.com/jeffknupp/sandman) litte
brother. Like `sandman`, Flask-Sandboy automatically generates REST APIs. Unlike
`sandman`, it does so from existing Flask-SQLAlchemy models.

**tl;dr Flask-Sandboy gives your models a RESTful HTTP endpoint automagically, with proper support for all HTTP methods. It takes two lines of code to use and has no dependencies.**

## Installation

Flask-Sandboy should be installed using `pip`:

```shell
$ pip install flask-sandboy
```

## Usage

Here is an example `runserver.py` for an existing Flask app with Flask-SQLAlchemy models:

```python
from flask import Flask
from models import Machine, Cloud, db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
db.init_app(app)
with app.app_context():
    db.create_all()
app.run(debug=True)
```

And here is that same app with RESTful endpoints automatically created and managed by Flask-Sandboy

```python
from flask import Flask
from flask.ext.sandboy import Sandboy

from models import Machine, Cloud, db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
db.init_app(app)
with app.app_context():
    db.create_all()
sandboy = Sandboy(app, db, [Cloud, Machine])
app.run(debug=True)
```

The only thing you need to do is instantiate the `Sandboy` class with your app,
your Flask-SQLAlchemy object (typically named `db`), and a list of Model classes
for which you want REST endpoints created.

Start the server and let's test out our new REST API:

```shell
$ http -vv -j POST localhost:5000/cloud name=first_cloud description="my first cloud"                                                                      master
POST /cloud HTTP/1.1
Accept: application/json
Accept-Encoding: gzip, deflate, compress
Content-Length: 56
Content-Type: application/json; charset=utf-8
Host: localhost:5000
User-Agent: HTTPie/0.8.0

{
    "description": "my first cloud",
    "name": "first_cloud"
}

HTTP/1.0 201 CREATED
Content-Length: 75
Content-Type: application/json
Date: Tue, 06 May 2014 13:57:52 GMT
Server: Werkzeug/0.9.4 Python/2.7.6

{
    "description": "my first cloud",
    "id": 1,
    "name": "first_cloud"
}
```

```shell
$ http localhost:5000/cloud/1                                                                                                                                       master
HTTP/1.0 200 OK
Content-Length: 75
Content-Type: application/json
Date: Tue, 06 May 2014 13:53:18 GMT
Server: Werkzeug/0.9.4 Python/2.7.6

{
    "description": "my first cloud",
    "id": 1,
    "name": "first_cloud"
}
```

```shell
$ http DELETE :5000/cloud/1                                                                                                                                master
HTTP/1.0 204 NO CONTENT
Content-Length: 0
Content-Type: text/html; charset=utf-8
Date: Tue, 06 May 2014 13:53:23 GMT
Server: Werkzeug/0.9.4 Python/2.7.6
```

All common HTTP methods are implemented (`HEAD`, `OPTIONS`, `GET`, `DELETE`, `POST`, `PATCH`, `PUT`) with proper HTTP status codes.

## Validating Requests

Flask-Sandboy comes with built-in request validation, ensuring that all fields
necessary to save the object to the database are present. Here's what happens
when we forget to include a field:

```shell
$ http -j POST :5000/cloud name="bad cloud"                                                                                                          develop
HTTP/1.0 403 FORBIDDEN
Content-Length: 45
Content-Type: application/json
Date: Tue, 06 May 2014 14:05:52 GMT
Server: Werkzeug/0.9.4 Python/2.7.6

{
    "message": "cloud.description required"
}
```

## Pagination

Flask-Sandboy supports pagination of results by default. Simply add a `<model_name>?page=2` to your
request to get paginated results. By default, 20 results per page are returned.

## TODO

I'll leave it up to the Issues tab to track this.

## Release History

### 0.0.3
 
* various bug fixes
* 100% test coverage
* documentation

### 0.0.2
 
* various bug fixes

### 0.0.1

* Initial release
