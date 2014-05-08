Introduction
============

``Flask-sandboy`` is a Flask extentsion that automagically creates RESTful HTTP
endpoints for your existing SQLAlchemy models. If you've ever written a Flask
application that was HTML-driven, then been asked to write a REST API for it,
you'll understand how pointless and repetitive the task seems.

Because REST APIs are stupid. 99% of them do the same thing regardless of problem
domain. Shouldn't we be able to just tell some library, "Hey, make a REST API
out of these models." I mean, you're passing the fields for each resource. What
else does it need?

Before ``Flask-sandboy``, creating a REST API for existing models required
effort. Now, it doesn't even require thought. With _two lines of code (one of which is an ``import``)_
you get a set of RESTful HTTP endpoints for your models.
