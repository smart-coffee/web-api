import os

from enum import Enum
from typing import List
from dotenv import load_dotenv, find_dotenv

from config.logger import logging, get_logger_name


logger = logging.getLogger(get_logger_name(__name__))


class Mode(Enum):
    PROD = ('prod', 'config/production.py')
    DEV = ('dev', 'config/development.py')
    TEST = ('test', 'config/testing.py')

    def __init__(self, mode_str, config_path):
        self._mode_str = mode_str
        self._config_path = config_path

    @property
    def mode_str(self):
        return self._mode_str

    @property
    def config_path(self):
        return self._config_path


def get_default_mode():
    return Mode.DEV


_available_environment_variables = {
    'MODE': None,
    'CERT_FILE': None,
    'KEY_FILE': None,
    'DB_USER': None,
    'DB_NAME': None,
    'DB_HOST': None,
    'DB_PW': None,
    'DB_PORT': None,
    'APP_PORT': None,
    'APP_HOST': None,
    'SECRET_KEY': None,
    'APP_URL_PREFIX': None,
    'SWAGGER_BASE_URL': None
}


def init_environment(env_path: str = None, debug: bool = True):
    if env_path:
        load_dotenv(dotenv_path=env_path)
    else:
        load_dotenv(find_dotenv())
    for key in _available_environment_variables.keys():
        _env_var = os.environ[key]
        if debug and len(_env_var) == 0:
            logger.warning('Environment variable "{}" is empty'.format(key))
        _available_environment_variables[key] = _env_var
    _replace_environment_mode(_available_environment_variables)


def get_env_vars() -> List[str]:
    return list(_available_environment_variables.keys())


def get_environment_mode():
    return _available_environment_variables['MODE']


def get_cert():
    return _available_environment_variables['CERT_FILE']


def get_key():
    return _available_environment_variables['KEY_FILE']


def get_db_user():
    return _available_environment_variables['DB_USER']


def get_db_name():
    return _available_environment_variables['DB_NAME']


def get_db_host():
    return _available_environment_variables['DB_HOST']


def get_db_pw():
    return _available_environment_variables['DB_PW']


def get_db_port():
    return _available_environment_variables['DB_PORT']


def get_app_host():
    return _available_environment_variables['APP_HOST']


def get_app_port():
    return _available_environment_variables['APP_PORT']


def get_secret_key():
    return _available_environment_variables['SECRET_KEY']


def get_app_url_prefix():
    return _available_environment_variables['APP_URL_PREFIX']


def get_swagger_base_url():
    return _available_environment_variables['SWAGGER_BASE_URL']


def _replace_environment_mode(params: dict):
    _chosen_config = get_default_mode()
    _possible_modes = '|'.join(map(lambda m: m.mode_str, list(Mode)))
    _help = 'app.py -m [{0}] OR app.py --mode [{0}]'.format(_possible_modes)

    for mode in Mode:
        if mode.mode_str == params['MODE']:
            _chosen_config = mode
            break

    logger.debug('Replaced {} with {}'.format(params['MODE'], _chosen_config))
    params['MODE'] = _chosen_config
    return params


if __name__ == "__main__":
    init_environment()
