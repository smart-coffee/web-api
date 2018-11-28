

from models import Role
from controllers.base_controller import _BaseController
from controllers.fixture_functions import run_role_fixture
from config.logger import logging, get_logger_name


logger = logging.getLogger(get_logger_name(__name__))


class RoleController(_BaseController):
    def __init__(self):
        super(RoleController, self).__init__(model_class=Role, resource_name='Role', fixture_function=run_role_fixture, create_request_fields=None)
