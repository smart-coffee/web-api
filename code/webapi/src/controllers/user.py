import uuid

from typing import List
from flask import request
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.security import check_password_hash, generate_password_hash
from email_validator import validate_email, EmailNotValidError

from models import User
from config.flask_config import ResourceNotFound, ResourceException
from controllers.request_model import get_edit_user_request_fields, get_register_user_request_fields
from controllers.fixture_functions import run_user_fixture
from utils.basic import is_dict_structure_equal
from config.logger import logging, get_logger_name
from config import FLASK_APP, DB

logger = logging.getLogger(get_logger_name(__name__))


class UserController:

    def get_by_id(self, resource_id: str, current_user:User) -> User:
        _user = User.query.filter_by(public_id=resource_id).first()
        if not _user:
            raise ResourceNotFound('User not found')
        run_user_fixture(_user)
        return _user

    def get_list(self, current_user:User) -> List[User]:
        _users = User.query.all()
        for _user in _users:
            if _user:
                run_user_fixture(_user)
        return _users
    
    def get_by_username(self, username: str, current_user: User=None) -> User:
        _user = User.query.filter_by(name=username).first()
        if not _user:
            raise ResourceNotFound('User not found')
        run_user_fixture(_user)
        return _user

    def edit_current_user(self, current_user:User) -> User:
        data = self._get_validated_request_body_as_json(template=get_edit_user_request_fields())

        self._try_edit_user_password(data=data, user=current_user)
        self._try_edit_user_email(data=data, user=current_user)
        self._try_edit_user_name(data=data, user=current_user)

        session = DB.session
        try:
            session.commit()
        except SQLAlchemyError as err:
            logger.error('Failed to edit current user: {}'.format(str(err)))
            session.rollback()
            raise err
        logger.info('Current user edited.')
        run_user_fixture(current_user)
        return current_user
    
    def create_user(self) -> User:
        data = self._get_validated_request_body_as_json(template=get_register_user_request_fields())

        new_user = User()
        new_user.email = self._get_validated_email(data['email'])
        new_user.name = self._get_validated_user_name(data['name'])
        new_user.password = self._encode_password(data['password'])
        new_user.public_id = self._generate_new_public_id()

        logger.debug('New transient user created: {0}, {1}, {2}'.format(new_user.name, new_user.email, new_user.public_id))

        session = DB.session
        try:
            session.add(new_user)
            session.commit()
        except SQLAlchemyError as err:
            logger.error('Failed to register user: {}'.format(str(err)))
            session.rollback()
            raise err
        logger.info('User {name} created ({id}).'.format(name=new_user.name, id=new_user.public_id))
        return new_user

    @staticmethod
    def _get_validated_request_body_as_json(template: dict):
        _data = request.get_json()
        if not is_dict_structure_equal(template, _data):
            raise ResourceException('Request body contains unknown key value pairs.')
        return _data

    @staticmethod
    def _try_edit_user_password(data: dict, user: User):
        new_password = data['new_password']
        old_password = data['old_password']

        old_password_confirmed = False
        if old_password:
            old_password = self._get_validated_password(old_password)
            old_password_confirmed = check_password_hash(user.password, old_password)
            if not old_password_confirmed:
                msg = 'The old password is not correct.'
                logger.error(msg)
                raise ResourceException(msg)

        if old_password and not new_password:
            msg = 'Request body does not contain the new password.'
            logger.error(msg)
            raise ResourceException(msg)
        if new_password and not old_password:
            msg = 'Request body does not contain the old password.'
            logger.error(msg)
            raise ResourceException(msg)

        new_password_differs = False
        if new_password:
            new_password = self._get_validated_password(new_password)
            new_password_differs = not check_password_hash(user.password, new_password)

        if old_password_confirmed and new_password_differs:
            logger.debug('Trying to change password of user {}'.format(user.public_id))
            hashed_password = generate_password_hash(new_password, method='sha256')
            user.password = hashed_password

    @staticmethod
    def _try_edit_user_email(data: dict, user: User):
        email = data['email']

        if email and email != user.email:
            logger.debug('Trying to change email of user {0} to {1}'.format(user.public_id, email))
            try:
                user.email = self._get_validated_email(email)
            except EmailNotValidError as err:
                raise ResourceException('Email {0} is not in a valid format: {1}'.format(email, str(err)))

    @staticmethod
    def _try_edit_user_name(data: dict, user: User):
        name = data['name']

        if name and name != user.name:
            logger.debug('Trying to change name of user {0} to {1}'.format(user.public_id, name))
            user.name = self._get_validated_user_name(name)

    @staticmethod
    def _get_validated_email(email:str) -> str:
        if not email:
            raise ResourceException('Email is missing.')
        validated_email = validate_email(email)
        return validated_email['email']
    
    @staticmethod
    def _get_validated_password(password:str) -> str:
        if not password:
            raise ResourceException('Password is missing.')
        if len(password) < 6:
            raise ResourceException('Password is to short. At least 6 characters.')
        return password

    @staticmethod    
    def _get_validated_user_name(name:str) -> str:
        if not name:
            raise ResourceException('Username is missing.')
        if len(name) < 6:
            raise ResourceException('Username is to short. At least 6 characters.')
        return name
    
    @staticmethod
    def _generate_new_public_id() -> str:
        return str(uuid.uuid4())

    def _encode_password(self, password:str) -> str:
        password = self._get_validated_password(password)
        encoded_password = generate_password_hash(password, method='sha256')
        return encoded_password
