import json

from typing import List

from flasgger import swag_from
from flask import Blueprint
from flask_restful import Api, marshal_with, Resource

from controllers.fixture_functions import run_coffee_brand_fixture
from controllers.coffee import CoffeeMachineController, CoffeeTypeController, CoffeeBrandController
from models import CoffeeMachine, User, CoffeeType, CoffeeBrand
from controllers.response_model import get_coffee_machine_fields, get_coffee_type_fields, get_coffee_brand_fields
from controllers.request_model import get_create_coffee_brand_request_fields
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
        coffee_machine = self.controller.create(current_user)
        serialized_coffee_machine = serialize(coffee_machine, get_coffee_machine_fields())
        json_coffee_machine = json.dumps(serialized_coffee_machine)
        response = get_post_response(obj=coffee_machine, body=json_coffee_machine, content_type='application/json', api='/{rsc}/machines'.format(rsc=API_PREFIX))
        return response


class CoffeeMachineResource(Resource):
    def __init__(self):
        self.controller = CoffeeMachineController()

    @token_required()
    @swag_from('/resources/coffee/description/coffee_machine_get.yml')
    @marshal_with(get_coffee_machine_fields())
    def get(self, coffee_machine_id, current_user: User) -> CoffeeMachine:
        return self.controller.get_by_id(coffee_machine_id, current_user)


class CoffeeTypeListResource(Resource):
    def __init__(self):
        self.controller = CoffeeTypeController()
    
    @token_required()
    @swag_from('/resources/coffee/description/coffee_type_list_get.yml')
    @marshal_with(get_coffee_type_fields())
    def get(self, current_user: User) -> List[CoffeeType]:
        return self.controller.get_list(current_user)
    
    @token_required(roles=['Administrator'])
    @swag_from('/resources/coffee/description/coffee_type_list_post.yml')
    def post(self, current_user: User) -> CoffeeType:
        coffee_type = self.controller.create(current_user)
        serialized_coffee_type = serialize(coffee_type, get_coffee_type_fields())
        json_coffee_type = json.dumps(serialized_coffee_type)
        response = get_post_response(obj=coffee_type, body=json_coffee_type, content_type='application/json', api='/{rsc}/types'.format(rsc=API_PREFIX))
        return response


class CoffeeTypeResource(Resource):
    def __init__(self):
        self.controller = CoffeeTypeController()

    @token_required()
    @swag_from('/resources/coffee/description/coffee_type_get.yml')
    @marshal_with(get_coffee_type_fields())
    def get(self, coffee_type_id, current_user: User) -> CoffeeType:
        return self.controller.get_by_id(coffee_type_id, current_user)


class CoffeeBrandListResource(Resource):
    def __init__(self):
        self.controller = CoffeeBrandController()

    @token_required()
    @swag_from('/resources/coffee/description/coffee_brand_list_get.yml')
    @marshal_with(get_coffee_brand_fields())
    def get(self, current_user: User) -> List[CoffeeBrand]:
        return self.controller.get_list(current_user)
    
    @token_required(roles=['Administrator'])
    @swag_from('/resources/coffee/description/coffee_brand_list_post.yml')
    def post(self, current_user: User) -> CoffeeBrand:
        coffee_brand = self.controller.create(current_user)
        serialized_coffee_brand = serialize(coffee_brand, get_coffee_brand_fields())
        json_coffee_brand = json.dumps(serialized_coffee_brand)
        response = get_post_response(obj=coffee_brand, body=json_coffee_brand, content_type='application/json', api='/{rsc}/brands'.format(rsc=API_PREFIX))
        return response


class CoffeeBrandResource(Resource):
    def __init__(self):
        self.controller = CoffeeBrandController()

    @token_required()
    @swag_from('/resources/coffee/description/coffee_brand_get.yml')
    @marshal_with(get_coffee_brand_fields())
    def get(self, coffee_brand_id, current_user: User) -> CoffeeBrand:
        return self.controller.get_by_id(coffee_brand_id, current_user)


api.add_resource(CoffeeMachineListResource, '/{rsc}/machines'.format(rsc=API_PREFIX))
api.add_resource(CoffeeMachineResource, '/{rsc}/machines/<int:coffee_machine_id>'.format(rsc=API_PREFIX))
api.add_resource(CoffeeTypeListResource, '/{rsc}/types'.format(rsc=API_PREFIX))
api.add_resource(CoffeeTypeResource, '/{rsc}/types/<int:coffee_type_id>'.format(rsc=API_PREFIX))
api.add_resource(CoffeeBrandListResource, '/{rsc}/brands'.format(rsc=API_PREFIX))
api.add_resource(CoffeeBrandResource, '/{rsc}/brands/<int:coffee_brand_id>'.format(rsc=API_PREFIX))
