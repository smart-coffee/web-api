from typing import List
from sqlalchemy.exc import SQLAlchemyError
from flask import request

from models import CoffeeMachine, User, CoffeeType, CoffeeBrand
from config.flask_config import ResourceNotFound
from controllers.fixture_functions import run_coffee_machine_fixture, run_coffee_type_fixture, run_coffee_brand_fixture
from controllers.request_model import get_create_coffee_machine_request_fields, get_create_coffee_type_request_fields, get_create_coffee_brand_request_fields
from config.logger import logging, get_logger_name
from utils.http import get_validated_request_body_as_json
from config import DB


logger = logging.getLogger(get_logger_name(__name__))


class CoffeeMachineController:
    def get_by_id(self, resource_id: int, current_user: User) -> CoffeeMachine:
        _coffee_machine = CoffeeMachine.query.filter_by(id=resource_id).first()
        if not _coffee_machine:
            logger.error('{user} tried to get coffee_machine {coffee_machine} and failed.'.format(user=current_user.id, coffee_machine=resource_id))
            raise ResourceNotFound('Coffee Machine not found')
        run_coffee_machine_fixture(_coffee_machine)
        logger.debug('User {user} requested coffee machine {coffee_machine}'.format(user=current_user.name, coffee_machine=_coffee_machine.name))
        return _coffee_machine
    
    def get_list(self, current_user: User) -> List[CoffeeMachine]:
        _coffee_machines = CoffeeMachine.query.all()
        for _coffee_machine in _coffee_machines:
            if _coffee_machine:
                run_coffee_machine_fixture(_coffee_machine)
        return _coffee_machines
    
    def create_coffee_machine(self, current_user: User) -> CoffeeMachine:
        data = get_validated_request_body_as_json(get_create_coffee_machine_request_fields())

        coffee_machine = CoffeeMachine()
        coffee_machine.name = data['name']
        coffee_machine.repository = data['repository']

        session = DB.session

        try:
            session.add(coffee_machine)
            session.commit()
        except SQLAlchemyError as err:
            logger.error('Failed to create coffee machine: {}'.format(str(err)))
            session.rollback()
            raise err
        logger.info('Coffee Machine {name} created ({id}).'.format(name=coffee_machine.name, id=coffee_machine.id))
        return coffee_machine


class CoffeeTypeController:
    def get_by_id(self, resource_id: int, current_user: User) -> CoffeeType:
        _coffee_type = CoffeeType.query.filter_by(id=resource_id).first()
        if not _coffee_type:
            logger.error('{user} tried to get Coffee Type {coffee_type} and failed.'.format(user=current_user.id, coffee_type=resource_id))
            raise ResourceNotFound('Coffee Machine not found')
        run_coffee_type_fixture(_coffee_type)
        logger.debug('User {user} requested Coffee Type {coffee_type}'.format(user=current_user.name, coffee_type=_coffee_type.name))
        return _coffee_type
    
    def get_list(self, current_user: User) -> List[CoffeeType]:
        _coffee_types = CoffeeType.query.all()
        for _coffee_type in _coffee_types:
            if _coffee_type:
                run_coffee_type_fixture(_coffee_type)
        return _coffee_types
    
    def create_coffee_type(self, current_user: User) -> CoffeeType:
        data = get_validated_request_body_as_json(get_create_coffee_type_request_fields())

        coffee_type = CoffeeType()
        coffee_type.name = data['name']

        session = DB.session

        try:
            session.add(coffee_type)
            session.commit()
        except SQLAlchemyError as err:
            logger.error('Failed to create coffee type: {}'.format(str(err)))
            session.rollback()
            raise err
        logger.info('Coffee Type {name} created ({id}).'.format(name=coffee_type.name, id=coffee_type.id))
        return coffee_type


class CoffeeBrandController:
    def get_by_id(self, resource_id: int, current_user: User) -> CoffeeBrand:
        _coffee_brand = CoffeeBrand.query.filter_by(id=resource_id).first()
        if not _coffee_brand:
            logger.error('{user} tried to get Coffee brand {coffee_brand} and failed.'.format(user=current_user.id, coffee_brand=resource_id))
            raise ResourceNotFound('Coffee Brand not found')
        run_coffee_brand_fixture(_coffee_brand)
        logger.debug('User {user} requested Coffee brand {coffee_brand}'.format(user=current_user.name, coffee_brand=_coffee_brand.name))
        return _coffee_brand
    
    def get_list(self, current_user: User) -> List[CoffeeBrand]:
        _coffee_brands = CoffeeBrand.query.all()
        for _coffee_brand in _coffee_brands:
            if _coffee_brand:
                run_coffee_brand_fixture(_coffee_brand)
        return _coffee_brands
    
    def create_coffee_brand(self, current_user: User) -> CoffeeBrand:
        data = get_validated_request_body_as_json(get_create_coffee_brand_request_fields())

        coffee_brand = CoffeeBrand()
        coffee_brand.name = data['name']

        session = DB.session

        try:
            session.add(coffee_brand)
            session.commit()
        except SQLAlchemyError as err:
            logger.error('Failed to create coffee brand: {}'.format(str(err)))
            session.rollback()
            raise err
        logger.info('Coffee brand {name} created ({id}).'.format(name=coffee_brand.name, id=coffee_brand.id))
        return coffee_brand

########
class CoffeeController:
    def __init__(self, model_class, resource_name, fixture_function, create_request_fields):
        self.model_class = model_class
        self.resource_name = resource_name
        self.fixture_function = fixture_function
        self.create_request_fields = create_request_fields
    
    def get_by_id(self, resource_id, current_user: User) -> object:
        obj = self.model_class.query.filter_by(id=resource_id).first()
        if not obj:
            logger.error('{user} tried to get {resource_name} {instance_name} and failed.'.format(user=current_user.id, resource_name=self.resource_name, instance_name=obj.get_id()))
            raise ResourceNotFound('{resource_name} not found'.format(resource_name=self.resource_name))
        self.fixture_function(obj)
        logger.debug('User {user} requested {resource_name} {instance_name}.'.format(user=current_user.id, resource_name=self.resource_name, instance_name=obj.get_id()))
        return obj

    def get_list(self, current_user: User) -> List[object]:
        obj_list = self.model_class.query.all()
        for obj in obj_list:
            if obj:
                self.fixture_function(obj)
        return obj_list
    
    def create(self, current_user: User) -> object:
        data = get_validated_request_body_as_json(self.create_request_fields)

        obj = self.create_object(data)

        session = DB.session
        try:
            session.add(obj)
            session.commit()
        except SQLAlchemyError as err:
            logger.error('Failed to create {resource_name}: {error}'.format(resource_name=self.resource_name, error=str(err)))
            session.rollback()
            raise err
        logger.info('{resource_name} {id} created.'.format(resource_name=self.resource_name, id=obj.get_id()))
        return obj

    def create_object(data: dict) -> object:
        pass