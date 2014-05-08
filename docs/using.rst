Using Flask-sandboy
===================

Here is an example ``runserver.py`` for an existing Flask app with Flask-SQLAlchemy models::

    from flask import Flask
    from models import Machine, Cloud, db

    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
    db.init_app(app)
    with app.app_context():
        db.create_all()
    app.run(debug=True)

And here is that same app with RESTful endpoints automatically created and managed by Flask-Sandboy::

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

The only thing you need to do is instantiate the ``Sandboy`` class with your app,
your Flask-SQLAlchemy object (typically named ``db``), and a list of Model classes
for which you want REST endpoints created.

Start the server and let's test out our new REST API::

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

    $ http DELETE :5000/cloud/1                                                                                                                                master
    HTTP/1.0 204 NO CONTENT
    Content-Length: 0
    Content-Type: text/html; charset=utf-8
    Date: Tue, 06 May 2014 13:53:23 GMT
    Server: Werkzeug/0.9.4 Python/2.7.6
    ````

All common HTTP methods are implemented (``HEAD``, ``OPTIONS``, ``GET``, ``DELETE``, ``POST``, ``PATCH``, ``PUT``) with proper HTTP status codes.

Verification
------------

``Flask-sandboy`` is even able to verify things like all fields being set on a
request (since it knows what fields your models has). If a request is missing a
field, it will return an error with a message that includes the name of the 
missing field to aid the client in debugging.

Pagination
----------

``Flask-sandboy`` also comes with support for pagination. Simply add ``/resource?page=3``
to your request to get paginated results. The default number of results per page
is 20, though this will be configurable in the future.
