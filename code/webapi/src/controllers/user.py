import uuid

from typing import List
from flask import request
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.security import check_password_hash, generate_password_hash
from email_validator import validate_email, EmailNotValidError

from models import User, Profile
from config.flask_config import ResourceNotFound, ResourceException
from controllers.request_model import get_edit_user_request_fields, get_register_user_request_fields, get_create_current_user_profile_request_fields, get_edit_current_user_profile_request_fields
from controllers.fixture_functions import run_user_fixture, run_profile_fixture
from controllers.base_controller import _BaseController
from utils.http import get_validated_request_body_as_json
from config.logger import logging, get_logger_name
from config import FLASK_APP, DB


logger = logging.getLogger(get_logger_name(__name__))


class CurrentUserController(_BaseController):
    def __init__(self):
        super(CurrentUserController, self).__init__(model_class=User, resource_name='User', fixture_function=run_user_fixture, edit_request_fields=get_edit_user_request_fields(), id_field='public_id')
        self.tools = UserTools()

    def get_by_username(self, username: str, current_user: User=None) -> User:
        _user = User.query.filter_by(name=username).first()
        if not _user:
            raise ResourceNotFound('User not found')
        run_user_fixture(_user)
        return _user

    def edit_object(self, object_to_edit: User, data: dict, current_user: User) -> User:
        self.tools._try_edit_user_password(data=data, user=object_to_edit)
        self.tools._try_edit_user_email(data=data, user=object_to_edit)
        self.tools._try_edit_user_name(data=data, user=object_to_edit)
        return object_to_edit


class CurrentUserProfileController(_BaseController):
    def __init__(self):
        super(CurrentUserProfileController, self).__init__(model_class=Profile, resource_name='Profile', fixture_function=run_profile_fixture, create_request_fields=get_create_current_user_profile_request_fields(), edit_request_fields=get_edit_current_user_profile_request_fields())
        self.tools = UserTools()
    
    def create_object(self, data: dict, current_user: User) -> Profile:
        profile = Profile()
        profile.name = data['name']
        profile.user = current_user
        profile.coffee_strength_in_percent = data['coffee_strength_in_percent']
        profile.water_in_percent = data['water_in_percent']
        return profile


class PublicUserController(_BaseController):
    def __init__(self):
        super(PublicUserController, self).__init__(model_class=User, resource_name='User', fixture_function=run_user_fixture, create_request_fields=get_register_user_request_fields(), id_field='public_id')
        self.tools = UserTools() 

    def create_object(self, data: dict, current_user: User) -> User:
        new_user = User()
        new_user.email = self.tools._get_validated_email(data['email'])
        new_user.name = self.tools._get_validated_user_name(data['name'])
        new_user.password = self.tools._encode_password(data['password'])
        new_user.public_id = self.tools._generate_new_public_id()
        return new_user


class UserTools:
    def _try_edit_user_password(self, data: dict, user: User):
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

    def _try_edit_user_email(self, data: dict, user: User):
        email = data['email']

        if email and email != user.email:
            logger.debug('Trying to change email of user {0} to {1}'.format(user.public_id, email))
            try:
                user.email = self._get_validated_email(email)
            except EmailNotValidError as err:
                raise ResourceException('Email {0} is not in a valid format: {1}'.format(email, str(err)))

    def _try_edit_user_name(self, data: dict, user: User):
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
