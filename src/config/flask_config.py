from typing import List
from flask import Flask, Blueprint, jsonify


# Flask Exceptions

class ResourceException(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None, headers: dict=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload
        self.headers = headers

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv


class ResourceNotFound(ResourceException):
    def __init__(self, message, payload=None, headers=None):
        ResourceException.__init__(self, message, 404, payload, headers)


class AuthenticationFailed(ResourceException):
    def __init__(self, message, payload=None, headers=None):
        ResourceException.__init__(self, message, 401, payload, headers)


class ForbiddenResourceException(ResourceException):
    def __init__(self, message, payload=None, headers=None):
        ResourceException.__init__(self, message, 403, payload, headers)


class ResourceNotImplemented(ResourceException):
    def __init__(self, message='Not implemented yet', payload=None, headers=None):
        ResourceException.__init__(self, message, 501, payload, headers)


def create_response(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    if error.headers:
        for k, v in error.headers.items():
            response.headers[k] = v
    return response


# Configuration

class FlaskExceptionConfig:
    def __init__(self, flask_app):
        self.app = flask_app

    def configure_handlers(self):
        self.register_exception(ResourceException)
        self.register_exception(ResourceNotImplemented)
        self.register_exception(ResourceNotFound)

    def register_exception(self, cls):
        self.app.register_error_handler(cls, lambda e: create_response(e))

    def configure_app(self):
        self.configure_handlers()


def apply_servername(response):
    response.headers['server'] = 'some_server'
    return response


def post_configuration(app: Flask, configs):
    app.after_request_funcs[None].append(apply_servername)
    for _config in configs:
        _config.configure_app()


def register_blueprints(app: Flask, blueprints: List[Blueprint]):
    for bp in blueprints:
        app.register_blueprint(bp)