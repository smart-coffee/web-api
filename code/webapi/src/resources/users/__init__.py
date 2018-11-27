import json

from flasgger import swag_from
from flask import Blueprint
from flask_restful import Api, marshal_with, Resource

from controllers.user import UserController
from models import User
from controllers.response_model import get_registered_user_details
from utils.http import token_required, get_post_response, serialize


API_PREFIX = 'users'
USER_BP = Blueprint('{rsc}_api'.format(rsc=API_PREFIX), __name__)
api = Api(USER_BP)


class CurrentUserResource(Resource):
    def __init__(self):
        self.controller = UserController()

    @token_required()
    @swag_from('/resources/users/description/current_user_get.yml')
    @marshal_with(get_registered_user_details())
    def get(self, current_user: User):
        return current_user

    @token_required()
    @swag_from('/resources/users/description/current_user_put.yml')
    @marshal_with(get_registered_user_details())
    def put(self, current_user: User):
        return self.controller.edit_current_user(current_user)


class PublicUserResource(Resource):
    def __init__(self):
        self.controller = UserController()
    
    @swag_from('/resources/users/description/public_user_post.yml')
    # Marshal will not work because of 'Response' object
    #@marshal_with(get_registered_user_details())
    def post(self):
        new_user = self.controller.create_user()
        serialized_user = serialize(new_user, get_registered_user_details())
        json_user = json.dumps(serialized_user)
        response = get_post_response(obj=new_user, body=json_user, content_type='application/json', api='/public/{rsc}'.format(rsc=API_PREFIX))
        return response



api.add_resource(CurrentUserResource, '/{rsc}/current'.format(rsc=API_PREFIX))
api.add_resource(PublicUserResource, '/public/{rsc}'.format(rsc=API_PREFIX))
