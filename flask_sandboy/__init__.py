"""Flask application that creates a RESTful API from SQLAlchemy models."""

from flask import Blueprint, jsonify

from flask_sandboy.service import WriteService, ReadService
from flask_sandboy.models import SerializableModel
from flask_sandboy.exception import (
    BadRequestException,
    ForbiddenException,
    NotAcceptableException,
    NotFoundException,
    ConflictException,
    ServerErrorException,
    NotImplementedException,
    ServiceUnavailableException)

__version__ = '0.0.3'


class Sandboy(object):
    """Main object for injecting RESTful HTTP endpoint."""
    def __init__(self, app, db, models, url_prefix=None, readonly=False):
        """Initialize and register the given *models*."""
        self.app = app
        self.db = db
        app.extensions['sandboy'] = self
        self.blueprint = None
        self.url_prefix = url_prefix
        self.readonly = readonly
        self.init_app(app, models)

    def init_app(self, app, models):
        """Initialize and register error handlers."""

        # pylint: disable=unused-variable
        self.blueprint = Blueprint('sandboy', __name__, url_prefix=self.url_prefix)

        @self.blueprint.errorhandler(BadRequestException)
        @self.blueprint.errorhandler(ForbiddenException)
        @self.blueprint.errorhandler(NotAcceptableException)
        @self.blueprint.errorhandler(NotFoundException)
        @self.blueprint.errorhandler(ConflictException)
        @self.blueprint.errorhandler(ServerErrorException)
        @self.blueprint.errorhandler(NotImplementedException)
        @self.blueprint.errorhandler(ServiceUnavailableException)
        def handle_application_error(error):
            """Handler used to send JSON error messages rather than default
            HTML ones."""
            response = jsonify(error.to_dict())
            response.status_code = error.code
            return response

        self.register(models)
        app.register_blueprint(self.blueprint)

    def register(self, cls_list):
        """Register a class to be given a REST API."""
        for cls in cls_list:
            serializable_model = type(
                cls.__name__ + 'Serializable',
                (cls, SerializableModel),
                {})

            service = ReadService if self.readonly else WriteService

            new_endpoint = type(
                cls.__name__ + 'Endpoint',
                (service,),
                {'__model__': serializable_model,
                 '__db__': self.db})
            view_func = new_endpoint.as_view(
                new_endpoint.__model__.__tablename__)
            self.blueprint.add_url_rule(
                '/' + new_endpoint.__model__.__tablename__,
                defaults={'resource_id': None},
                view_func=view_func)
            self.blueprint.add_url_rule(
                '/{resource}/<resource_id>'.format(
                    resource=new_endpoint.__model__.__tablename__),
                view_func=view_func)
