import datetime
import time

from typing import List
from flask import request

from models import User, Job, CoffeeMachine
from controllers.base_controller import _BaseController
from controllers.coffee import CoffeeMachineController, CoffeeProductController
from controllers.user import UserController
from controllers.fixture_functions import run_job_fixture
from controllers.request_model import get_create_job_request_fields, get_edit_job_request_fields, get_create_current_user_job_request_fields
from config.logger import logging, get_logger_name


logger = logging.getLogger(get_logger_name(__name__))


class JobController(_BaseController):
    def __init__(self):
        super(JobController, self).__init__(model_class=Job, resource_name='Job', fixture_function=run_job_fixture, create_request_fields=get_create_job_request_fields(), edit_request_fields=get_edit_job_request_fields())
        self.coffee_machine_controller = CoffeeMachineController()
        self.coffee_product_controller = CoffeeProductController()
        self.user_controller = UserController()
    
    def get_list_statement(self, current_user: User) -> List[Job]:
        coffee_machine_name = request.args.get('coffee_machine_name')
        square = request.args.get('square')
        jobs = super().get_list_statement(current_user)

        # Filter if square filter is on
        if not (square is None):
            if square == "true":
                jobs = [job for job in jobs if not (job.square_date is None)]
            else:
                jobs = [job for job in jobs if job.square_date is None]

        # Filter if coffee machine filter is on
        if not (coffee_machine_name is None):
            coffee_machine = CoffeeMachine.query.filter_by(name=coffee_machine_name).first()
            if coffee_machine is None:
                logger.debug('Coffee Machine {} does not exist. Response list will be empty.'.format(coffee_machine_name))
                return []
            coffee_machine_id = coffee_machine.get_id()
            jobs = [job for job in jobs if job.coffee_machine.id == coffee_machine_id]

        return jobs

    def create_object(self, data: dict, current_user: User) -> Job:
        job = Job()
        # in seconds
        current_time = time.time()
        job.create_date = current_time
        job.square_date = None
        job.coffee_strength_in_percent = data['coffee_strength_in_percent']
        job.water_in_percent = data['water_in_percent']
        job.price = data['price']
        job.doses = data['doses']

        coffee_machine = self.coffee_machine_controller.get_by_id(data['coffee_machine_id'], current_user, False)
        job.coffee_machine = coffee_machine

        coffee_product = self.coffee_product_controller.get_by_id(data['coffee_product_id'], current_user, False)
        job.coffee_product = coffee_product

        user = self._get_user(current_user)
        job.user = user

        return job
    
    def edit_object(self, object_to_edit: Job, data: dict, current_user: User) -> Job:
        object_to_edit.create_date = data['create_date']
        object_to_edit.square_date = data['square_date']
        object_to_edit.coffee_strength_in_percent = data['coffee_strength_in_percent']
        object_to_edit.water_in_percent = data['water_in_percent']
        object_to_edit.price = data['price']
        object_to_edit.doses = data['doses']

        coffee_machine = self.coffee_machine_controller.get_by_id(data['coffee_machine_id'], current_user, False)
        object_to_edit.coffee_machine = coffee_machine

        coffee_product = self.coffee_product_controller.get_by_id(data['coffee_product_id'], current_user, False)
        object_to_edit.coffee_product = coffee_product

        user = self._get_user(current_user)
        object_to_edit.user = user

        return object_to_edit
    
    def _get_user(self, current_user: User) -> User:
        return self.user_controller.get_by_id(data['user_id'], current_user, False)


class CurrentUserJobController(JobController):
    def __init__(self):
        super(CurrentUserJobController, self).__init__()
        self.create_request_fields = get_create_current_user_job_request_fields()
    
    def get_list_statement(self, current_user: User) -> List[Job]:
        jobs = super().get_list_statement(current_user)
        jobs = [job for job in jobs if job.user.id == current_user.id]
        return jobs

    def _get_user(self, current_user: User) -> User:
        return current_user
    
    def edit(self, resource_id, current_user: User=None) -> Job:
        raise NotImplementedError()
    
    def delete(self, resource_id, current_user: User=None):
        raise NotImplementedError