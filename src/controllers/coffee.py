from typing import List

from models import User, CoffeeMachine, CoffeeType, CoffeeBrand, CoffeeProduct
from controllers.base_controller import _BaseController
from controllers.fixture_functions import run_coffee_machine_fixture, run_coffee_type_fixture, run_coffee_brand_fixture, run_coffee_product_fixture
from controllers.request_model import get_create_coffee_machine_request_fields, get_create_coffee_type_request_fields, get_create_coffee_brand_request_fields, get_create_coffee_product_request_fields
from config.logger import logging, get_logger_name


logger = logging.getLogger(get_logger_name(__name__))


class CoffeeBrandController(_BaseController):
    def __init__(self):
        super(CoffeeBrandController, self).__init__(model_class=CoffeeBrand, resource_name='Coffee Brand', fixture_function=run_coffee_brand_fixture, create_request_fields=get_create_coffee_brand_request_fields())
    
    def create_object(self, data: dict, current_user: User) -> CoffeeBrand:
        coffee_brand = CoffeeBrand()
        coffee_brand.name = data['name']
        return coffee_brand


class CoffeeTypeController(_BaseController):
    def __init__(self):
        super(CoffeeTypeController, self).__init__(model_class=CoffeeType, resource_name='Coffee Type', fixture_function=run_coffee_type_fixture, create_request_fields=get_create_coffee_type_request_fields())
    
    def create_object(self, data: dict, current_user: User) -> CoffeeType:
        coffee_type = CoffeeType()
        coffee_type.name = data['name']
        return coffee_type


class CoffeeMachineController(_BaseController):
    def __init__(self):
        super(CoffeeMachineController, self).__init__(model_class=CoffeeMachine, resource_name='Coffee Machine', fixture_function=run_coffee_machine_fixture, create_request_fields=get_create_coffee_machine_request_fields())
    
    def create_object(self, data: dict, current_user: User) -> CoffeeMachine:
        coffee_machine = CoffeeMachine()
        coffee_machine.name = data['name']
        coffee_machine.repository = data['repository']
        return coffee_machine


class CoffeeProductController(_BaseController):
    def __init__(self):
        super(CoffeeProductController, self).__init__(model_class=CoffeeProduct, resource_name='Coffee Product', fixture_function=run_coffee_product_fixture, create_request_fields=get_create_coffee_product_request_fields())
        self.type_controller = CoffeeTypeController()
        self.brand_controller = CoffeeBrandController()

    def create_object(self, data: dict, current_user: User) -> CoffeeProduct:
        coffee_product = CoffeeProduct()
        coffee_product.name = data['name']

        coffee_brand = self.brand_controller.get_by_id(data['coffee_brand_id'], current_user, False)
        coffee_product.coffee_brand = coffee_brand

        coffee_type = self.type_controller.get_by_id(data['coffee_type_id'], current_user, False)
        coffee_product.coffee_type = coffee_type

        return coffee_product