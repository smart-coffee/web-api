from flasgger import swag_from
from flask import Blueprint
from flask_restful import Api, marshal_with, Resource

from controllers.user import UserController
from models import User
from controllers.response_model import get_registered_user_details
from utils.http import token_required


API_PREFIX = 'user'
USER_BP = Blueprint('{rsc}_api'.format(rsc=API_PREFIX), __name__)
api = Api(USER_BP)


class _ControllerBased:
    def __init__(self):
        self.controller = UserController()


class CurrentUserResource(Resource, _ControllerBased):
    @token_required
    @swag_from('/resources/user/description/current_user_get.yml')
    @marshal_with(get_registered_user_details())
    def get(self, current_user: User):
        return current_user

    @token_required
    @swag_from('/resources/user/description/current_user_put.yml')
    @marshal_with(get_registered_user_details())
    def put(self, current_user: User):
        return self.controller.edit_current_user(current_user)


api.add_resource(CurrentUserResource, '/{rsc}/current'.format(rsc=API_PREFIX))
