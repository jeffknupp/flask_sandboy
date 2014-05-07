"""Base service for all RESTful endpoints."""
from flask import request, jsonify, make_response
from flask.views import MethodView

from flask_sandboy.models import verify_fields
from flask_sandboy.exception import NotFoundException

class Service(MethodView):
    """Base class for all resources."""

    __model__ = None
    __db__ = None

    def get(self, resource_id):
        """Return response to HTTP GET request."""
        if resource_id is None:
            return self._all_resources()
        else:
            resource = self._resource(resource_id)
            if not resource:
                raise NotFoundException
            return jsonify(resource.to_dict())

    def _all_resources(self):
        """Return all resources of this type as a JSON list."""
        if not 'page' in request.args:
            resources = self.__db__.session.query(self.__model__).all()
        else:
            resources = self.__model__.query.paginate(int(request.args['page'])).items
        return jsonify({'resources': [resource.to_dict() for resource in resources]})

    @verify_fields
    def post(self, resource_id=None):
        """Return response to HTTP POST request."""
        # pylint: disable=unused-argument
        resource = self.__model__.query.filter_by(**request.json).first()
        # resource already exists; don't create it again
        if resource:
            return self._no_content_response()
        instance = self.__model__(**request.json) #pylint: disable=not-callable
        self.__db__.session.add(instance)
        self.__db__.session.commit()
        return self._created_response(instance.to_dict())

    def delete(self, resource_id):
        """Return response to HTTP DELETE request."""
        instance = self._resource(resource_id)
        self.__db__.session.delete(instance)
        self.__db__.session.commit()
        return self._no_content_response()

    @verify_fields
    def put(self, resource_id):
        """Return response to HTTP PUT request."""
        instance = self._resource(resource_id)
        if instance is None:
            instance = self.__model__(**request.json) #pylint: disable=not-callable
        else:
            instance.from_dict(request.json)
        self.__db__.session.add(instance)
        self.__db__.session.commit()
        return self._created_response(instance.to_dict())

    @verify_fields
    def patch(self, resource_id):
        """Return response to HTTP PATCH request."""
        resource = self._resource(resource_id)
        resource.from_dict(request.json)
        self.__db__.session.add(resource)
        self.__db__.session.commit()
        return self._created_response(resource.to_dict())

    def _resource(self, resource_id):
        """Return resource represented by this *resource_id*."""
        resource = self.__db__.session.query(self.__model__).get(resource_id)
        if not resource:
            return None
        return resource

    @staticmethod
    def _no_content_response():
        """Return an HTTP 204 "No Content" response."""
        response = make_response()
        response.status_code = 204
        return response

    @staticmethod
    def _created_response(resource):
        """Return an HTTP 201 "Created" response."""
        response = jsonify(resource)
        response.status_code = 201
        return response
