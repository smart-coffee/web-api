import json

from typing import List

from flasgger import swag_from
from flask import Blueprint
from flask_restful import Api, marshal_with, Resource

from controllers.coffee import CoffeeMachineController
from models import CoffeeMachine, User
from controllers.response_model import get_coffee_machine_fields
from utils.http import token_required, get_post_response, serialize


API_PREFIX = 'coffee'
COFFEE_BP = Blueprint('{rsc}_api'.format(rsc=API_PREFIX), __name__)
api = Api(COFFEE_BP)


class CoffeeMachineListResource(Resource):
    def __init__(self):
        self.controller = CoffeeMachineController()

    @token_required()
    @swag_from('/resources/coffee/description/coffee_machine_list_get.yml')
    @marshal_with(get_coffee_machine_fields())
    def get(self, current_user: User) -> List[CoffeeMachine]:
        return self.controller.get_list(current_user)
    
    @token_required(roles=['Administrator'])
    @swag_from('/resources/coffee/description/coffee_machine_list_post.yml')
    def post(self, current_user: User) -> CoffeeMachine:
        coffee_machine = self.controller.create_coffee_machine(current_user)
        serialized_coffee_machine = serialize(coffee_machine, get_coffee_machine_fields())
        json_coffee_machine = json.dumps(serialized_coffee_machine)
        response = get_post_response(obj=coffee_machine, body=json_coffee_machine, content_type='application/json', api='/{rsc}/machines'.format(rsc=API_PREFIX))
        return response


api.add_resource(CoffeeMachineListResource, '/{rsc}/machines'.format(rsc=API_PREFIX))
