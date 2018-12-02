import uuid

from typing import List
from flask import request
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.security import check_password_hash, generate_password_hash
from email_validator import validate_email, EmailNotValidError, EmailSyntaxError

from models import User, Profile, Role, Job
from config.flask_config import ResourceNotFound, ResourceException, ForbiddenResourceException
from controllers.request_model import get_edit_current_user_request_fields, get_register_user_request_fields, get_create_current_user_profile_request_fields, get_edit_current_user_profile_request_fields, get_create_user_request_fields, get_edit_user_request_fields, get_create_user_profile_request_fields
from controllers.fixture_functions import run_user_fixture, run_profile_fixture
from controllers.base_controller import _BaseController
from utils.http import get_validated_request_body_as_json
from config.logger import logging, get_logger_name
from config import FLASK_APP, DB


logger = logging.getLogger(get_logger_name(__name__))


class CurrentUserController(_BaseController):
    def __init__(self):
        super(CurrentUserController, self).__init__(model_class=User, resource_name='User', fixture_function=run_user_fixture, edit_request_fields=get_edit_current_user_request_fields(), id_field='public_id')
        self.tools = UserTools()

    def get_by_username(self, username: str, current_user: User=None) -> User:
        _user = User.query.filter_by(name=username).first()
        if not _user:
            raise ResourceNotFound('User not found')
        run_user_fixture(_user)
        return _user

    def edit_object(self, object_to_edit: User, data: dict, current_user: User) -> User:
        if object_to_edit.public_id != current_user.public_id:
            raise ForbiddenResourceException('User {0} can not edit user {1}'.format(current_user.public_id, object_to_edit.public_id))
        self.tools._try_edit_user_password(data=data, user=object_to_edit)
        self.tools._try_edit_user_email(data=data, user=object_to_edit)
        self.tools._try_edit_user_name(data=data, user=object_to_edit)
        return object_to_edit


class CurrentUserProfileController(_BaseController):
    def __init__(self):
        super(CurrentUserProfileController, self).__init__(model_class=Profile, resource_name='Profile', fixture_function=run_profile_fixture, create_request_fields=get_create_current_user_profile_request_fields(), edit_request_fields=get_edit_current_user_profile_request_fields())
        self.tools = UserTools()
    
    def get_single_statement(self, criteria, current_user: User) -> Profile:
        profile = super().get_single_statement(criteria, current_user)
        if not profile:
            return None
        return profile if profile.user.id == current_user.id else None
    
    def get_list_statement(self, current_user: User) -> List[Profile]:
        profiles = super().get_list_statement(current_user)
        user_profiles = []
        for p in profiles:
            if p.user.id == current_user.id:
                user_profiles.append(p)
        return user_profiles
    
    def create_object(self, data: dict, current_user: User) -> Profile:
        profile = Profile()
        profile.name = data['name']
        profile.user = current_user
        profile.coffee_strength_in_percent = data['coffee_strength_in_percent']
        profile.water_in_percent = data['water_in_percent']
        return profile
    
    def edit_object(self, object_to_edit: Profile, data: dict, current_user: User) -> Profile:
        if object_to_edit.user.id != current_user.id:
            raise ForbiddenResourceException('User {0} can not edit profile {1}'.format(current_user.public_id, object_to_edit.id))
        object_to_edit.name = data['name']
        object_to_edit.coffee_strength_in_percent = data['coffee_strength_in_percent']
        object_to_edit.water_in_percent = data['water_in_percent']
        return object_to_edit


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


class UserController(_BaseController):
    def __init__(self):
        super(UserController, self).__init__(model_class=User, resource_name='User', fixture_function=run_user_fixture, create_request_fields=get_create_user_request_fields(), edit_request_fields=get_edit_user_request_fields(), id_field='public_id')
        self.tools = UserTools()

    def create_object(self, data: dict, current_user: User) -> User:
        new_user = User()
        new_user.email = self.tools._get_validated_email(data['email'])
        new_user.name = self.tools._get_validated_user_name(data['name'])
        new_user.password = self.tools._encode_password(data['password'])
        new_user.public_id = self.tools._generate_new_public_id()

        roles = data['roles']
        if (not (roles is None)) and len(roles) > 0:
            role_id = roles[0]
            role = Role.query.filter_by(id=role_id).first()
            if role is None:
                raise ResourceNotFound('Given role with id {} not found.'.format(role_id))
            new_user.role = role

        return new_user
    
    def edit_object(self, object_to_edit: User, data: dict, current_user: User) -> User:
        object_to_edit.password = self.tools._encode_password(data['password'])
        self.tools._try_edit_user_email(data=data, user=object_to_edit)
        self.tools._try_edit_user_name(data=data, user=object_to_edit)

        roles = data['roles']
        if (not (roles is None)) and len(roles) > 0:
            role_id = roles[0]
            role = Role.query.filter_by(id=role_id).first()
            if role is None:
                raise ResourceNotFound('Given role with id {} not found.'.format(role_id))
            object_to_edit.role = role
        else:
            object_to_edit.role = None

        return object_to_edit

    def delete_orphan_records(self, criteria, current_user: User):
        user = User.query.filter_by(**criteria).first()
        Profile.query.filter_by(user_id_fk=user.id).delete()
        Job.query.filter_by(user_id_fk=user.id).delete()


class UserProfileController(_BaseController):
    def __init__(self):
        super(UserProfileController, self).__init__(model_class=Profile, resource_name='Profile', fixture_function=run_profile_fixture, create_request_fields=get_create_user_profile_request_fields())
        self.tools = UserTools()
    
    def validate_single_result(self, result: Profile, **kwargs):
        acutal_public_id = result.user.public_id
        expected_public_id = kwargs['public_id']
        if acutal_public_id != expected_public_id:
            raise ForbiddenResourceException('Tried to get a profile that belongs to user {0} as user {1}'.format(acutal_public_id, expected_public_id))
    
    def get_list_statement(self, current_user: User, **kwargs) -> List[Profile]:
        user = self._get_user(**kwargs)
        return user.profiles

    def create_object(self, data: dict, current_user: User, **kwargs) -> Profile:
        profile = Profile()
        profile.name = data['name']
        profile.user = self._get_user(**kwargs)
        profile.coffee_strength_in_percent = data['coffee_strength_in_percent']
        profile.water_in_percent = data['water_in_percent']
        return profile

    def _get_user(self, **kwargs):
        public_id = kwargs['public_id']
        if public_id is None:
            raise ResourceException('Public ID is missing.')
        user = User.query.filter_by(public_id=public_id).first()
        if user is None:
            raise ResourceNotFound('User with public id {} not found.'.format(public_id))
        return user


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
            user.email = self._get_validated_email(email)
            

    def _try_edit_user_name(self, data: dict, user: User):
        name = data['name']

        if name and name != user.name:
            logger.debug('Trying to change name of user {0} to {1}'.format(user.public_id, name))
            user.name = self._get_validated_user_name(name)

    @staticmethod
    def _get_validated_email(email:str) -> str:
        if not email:
            raise ResourceException('Email is missing.')
        try:
            validated_email = validate_email(email)
        except EmailNotValidError as err:
            raise ResourceException('Email {0} is not in a valid format: {1}'.format(email, str(err)))
        except EmailSyntaxError as err:
            raise ResourceException('Email {0} is not in a valid syntax: {1}'.format(email, str(err)))
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
