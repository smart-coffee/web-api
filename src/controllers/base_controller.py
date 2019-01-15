from typing import List
from sqlalchemy.exc import SQLAlchemyError
from flask import request

from models import User
from config.flask_config import ResourceNotFound, DataStorageException
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
    
    def get_by_id(self, resource_id, current_user: User, autoflush=False, **kwargs) -> object:
        criteria= { self.id_field:resource_id }
        obj = self.get_single_statement(criteria, current_user, autoflush, **kwargs)
        if not obj:
            logger.error('{user} tried to get {resource_name} {instance_name} and failed.'.format(user=current_user.get_id(), resource_name=self.resource_name, instance_name=resource_id))
            raise ResourceNotFound('{resource_name} nicht gefunden.'.format(resource_name=self.resource_name))
        self.validate_single_result(obj, **kwargs)
        self.fixture_function(obj)
        logger.debug('User {user} requested {resource_name} {instance_name}.'.format(user=current_user.id, resource_name=self.resource_name, instance_name=obj.get_id()))
        return obj

    def get_single_statement(self, criteria, current_user: User, autoflush: bool, **kwargs) -> object:
        if autoflush == False:
            session = DB.session
            with session.no_autoflush:
                result = session.query(self.model_class).filter_by(**criteria).first()
        else:
            result = self.model_class.query.filter_by(**criteria).first()
        return result

    def validate_single_result(self, result, **kwargs):
        pass

    def get_list(self, current_user: User, **kwargs) -> List[object]:
        obj_list = self.get_list_statement(current_user, **kwargs)
        for obj in obj_list:
            if obj:
                self.fixture_function(obj)
        return obj_list
    
    def get_list_statement(self, current_user: User, **kwargs) -> List[object]:
        return self.model_class.query.all()

    def create(self, current_user: User=None, **kwargs) -> object:
        data = get_validated_request_body_as_json(self.create_request_fields)

        obj = self.create_object(data, current_user, **kwargs)

        session = DB.session
        try:
            session.add(obj)
            session.commit()
        except SQLAlchemyError as err:
            logger.error('Failed to create {resource_name}: {error}'.format(resource_name=self.resource_name, error=str(err)))
            session.rollback()
            raise DataStorageException(message='Der Nutzer ist möglicherweise schon vorhanden.')
        logger.info('{resource_name} {id} created.'.format(resource_name=self.resource_name, id=obj.get_id()))
        self.fixture_function(obj)
        return obj

    def create_object(self, data: dict, current_user: User, **kwargs) -> object:
        raise NotImplementedError()

    def edit(self, resource_id, current_user: User=None, **kwargs) -> object:
        obj_by_id = self.get_by_id(resource_id=resource_id, current_user=current_user, **kwargs)
        data = get_validated_request_body_as_json(template=self.edit_request_fields)

        obj = self.edit_object(object_to_edit=obj_by_id, data=data, current_user=current_user, **kwargs)

        session = DB.session
        try:
            session.commit()
        except SQLAlchemyError as err:
            logger.error('Failed to edit {resource_name}: {error}'.format(resource_name=self.resource_name, error=str(err)))
            session.rollback()
            raise err
        logger.info('{resource_name} {id} edited.'.format(resource_name=self.resource_name, id=obj.get_id()))
        self.fixture_function(obj)
        return obj
    
    def edit_object(self, object_to_edit, data: dict, current_user: User, **kwargs) -> object:
        raise NotImplementedError()
    
    def delete(self, resource_id, current_user: User=None, **kwargs):
        obj_by_id = self.get_by_id(resource_id=resource_id, current_user=current_user, **kwargs)
        criteria= { self.id_field:resource_id }
        self.delete_orphan_records(criteria, current_user)
        self.model_class.query.filter_by(**criteria).delete()

        session = DB.session
        try:
            session.commit()
        except SQLAlchemyError as err:
            logger.error('Failed to delete {resource_name}: {error}'.format(resource_name=self.resource_name, error=str(err)))
            session.rollback()
            raise err
        logger.info('{resource_name} {id} deleted.'.format(resource_name=self.resource_name, id=resource_id))

    def delete_orphan_records(self, criteria, current_user: User, **kwargs):
        pass