from typing import List

from models import CoffeeMachine, User, CoffeeType, CoffeeBrand
from controllers.base_controller import _BaseController
from controllers.fixture_functions import run_coffee_machine_fixture, run_coffee_type_fixture, run_coffee_brand_fixture
from controllers.request_model import get_create_coffee_machine_request_fields, get_create_coffee_type_request_fields, get_create_coffee_brand_request_fields
from config.logger import logging, get_logger_name
from utils.http import get_validated_request_body_as_json


logger = logging.getLogger(get_logger_name(__name__))


class CoffeeBrandController(_BaseController):
    def __init__(self):
        super(CoffeeBrandController, self).__init__(model_class=CoffeeBrand, resource_name='Coffee Brand', fixture_function=run_coffee_brand_fixture, create_request_fields=get_create_coffee_brand_request_fields())
    
    def create_object(self, data: dict) -> CoffeeBrand:
        coffee_brand = CoffeeBrand()
        coffee_brand.name = data['name']
        return coffee_brand


class CoffeeTypeController(_BaseController):
    def __init__(self):
        super(CoffeeTypeController, self).__init__(model_class=CoffeeType, resource_name='Coffee Type', fixture_function=run_coffee_type_fixture, create_request_fields=get_create_coffee_type_request_fields())
    
    def create_object(self, data: dict) -> CoffeeType:
        coffee_type = CoffeeType()
        coffee_type.name = data['name']
        return coffee_type


class CoffeeMachineController(_BaseController):
    def __init__(self):
        super(CoffeeMachineController, self).__init__(model_class=CoffeeMachine, resource_name='Coffee Machine', fixture_function=run_coffee_machine_fixture, create_request_fields=get_create_coffee_machine_request_fields())
    
    def create_object(self, data: dict) -> CoffeeMachine:
        coffee_machine = CoffeeMachine()
        coffee_machine.name = data['name']
        coffee_machine.repository = data['repository']
        return coffee_machine
