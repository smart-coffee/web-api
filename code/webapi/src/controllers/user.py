from typing import List
from flask import request
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.security import check_password_hash, generate_password_hash
from email_validator import validate_email, EmailNotValidError

from models import User
from config.flask_config import ResourceNotFound, ResourceException
from controllers.request_model import get_user_request_fields
from controllers.fixture_functions import run_user_fixture
from utils.basic import is_dict_structure_equal
from config.logger import logging, get_logger_name
from config import get_db_session, FLASK_APP

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

    def edit_current_user(self, current_user:User) -> User:
        data = request.get_json()
        if not is_dict_structure_equal(get_user_request_fields(), data):
            raise ResourceException('Request body contains unknown key value pairs.')

        self._try_edit_user_password(data=data, user=current_user)
        self._try_edit_user_email(data=data, user=current_user)
        self._try_edit_user_name(data=data, user=current_user)

        session = get_db_session(FLASK_APP)
        try:
            session.commit()
        except SQLAlchemyError as err:
            logger.error('Failed to edit current user: {}'.format(str(err)))
            session.rollback()
            raise err
        logger.info('Current user edited.')
        run_user_fixture(current_user)
        return current_user

    @staticmethod
    def _try_edit_user_password(data: dict, user: User):
        new_password = data['new_password']
        old_password = data['old_password']

        old_password_confirmed = False
        if old_password:
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
                validated_email = validate_email(email)
                user.email = validated_email['email']
            except EmailNotValidError as err:
                raise ResourceException('Email {0} is not in a valid format: {1}'.format(email, str(err)))

    @staticmethod
    def _try_edit_user_name(data: dict, user: User):
        name = data['name']

        if name and name != user.name:
            logger.debug('Trying to change name of user {0} to {1}'.format(user.public_id, name))
            user.name = name
