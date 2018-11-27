from typing import List

from flasgger import swag_from
from flask import Blueprint
from flask_restful import Api, marshal_with, Resource

from controllers.role import RoleController
from models import User, Role
from controllers.response_model import get_role_fields
from utils.http import token_required


API_PREFIX = 'roles'
ROLE_BP = Blueprint('{rsc}_api'.format(rsc=API_PREFIX), __name__)
api = Api(ROLE_BP)


class RoleResource(Resource):
    def __init__(self):
        self.controller = RoleController()

    @token_required(roles=['Administrator'])
    @swag_from('/resources/roles/description/roles_get.yml')
    @marshal_with(get_role_fields())
    def get(self, current_user: User) -> List[Role]:
        return self.controller.get_list(current_user)


api.add_resource(RoleResource, '/{rsc}'.format(rsc=API_PREFIX))
