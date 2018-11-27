from typing import List
from sqlalchemy.exc import SQLAlchemyError

from models import Role, User
from config.flask_config import ResourceNotFound
from controllers.fixture_functions import run_role_fixture
from config.logger import logging, get_logger_name


logger = logging.getLogger(get_logger_name(__name__))


class RoleController:
    def get_by_id(self, resource_id: int, current_user: User) -> Role:
        _role = Role.query.filter_by(id=resource_id).first()
        if not _role:
            logger.error('{user} tried to get role {role} and failed.'.format(user=current_user.id, role=resource_id))
            raise ResourceNotFound('Role not found')
        run_role_fixture(_role)
        logger.info('User {user} requested Role {role}'.format(user=current_user.name, role=role.name))
        return _role
    
    def get_list(self, current_user: User) -> List[Role]:
        _roles = Role.query.all()
        for _role in _roles:
            if _role:
                run_role_fixture(_role)
        return _roles

