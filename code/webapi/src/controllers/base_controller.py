from typing import List
from sqlalchemy.exc import SQLAlchemyError
from flask import request

from models import User
from config.flask_config import ResourceNotFound
from config.logger import logging, get_logger_name
from utils.http import get_validated_request_body_as_json
from config import DB


logger = logging.getLogger(get_logger_name(__name__))


class _BaseController:
    def __init__(self, model_class, resource_name, fixture_function, create_request_fields=None, edit_request_fields=None, id_field='id'):
        self.model_class = model_class
        self.resource_name = resource_name
        self.fixture_function = fixture_function
        self.create_request_fields = create_request_fields
        self.edit_request_fields = edit_request_fields
        self.id_field = id_field
    
    def get_by_id(self, resource_id, current_user: User) -> object:
        criteria= { self.id_field:resource_id }
        obj = self.model_class.query.filter_by(**criteria).first()
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
    
    def create(self, current_user: User=None) -> object:
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
        self.fixture_function(obj)
        return obj

    def create_object(self, data: dict) -> object:
        raise NotImplementedError()

    def edit(self, obj, current_user: User=None) -> object:
        data = get_validated_request_body_as_json(template=self.edit_request_fields)

        obj = self.edit_object(obj, data)

        session = DB.session
        try:
            session.commit()
        except SQLAlchemyError as err:
            logger.error('Failed to edit {resource_name}: {error}'.format(resource_name=self.resource_name, error=str(err)))
            session.rollback()
            raise err
        logger.info('{resource_name} {id} created.'.format(resource_name=self.resource_name, id=obj.get_id()))
        self.fixture_function(obj)
        return obj
    
    def edit_object(self, object_to_edit, data: dict) -> object:
        raise NotImplementedError()