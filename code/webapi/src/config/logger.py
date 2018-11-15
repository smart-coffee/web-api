import logging.handlers
import os
import errno

_LOG_DIR = 'logs'

if not os.path.isdir(_LOG_DIR):
    try:
        os.makedirs(_LOG_DIR)
    except OSError as exc:  # Guard against race condition
        if exc.errno != errno.EEXIST:
            raise


def get_logger_name(name=None):
    if name:
        return 'app.{}'.format(name)
    return 'app'


logger = logging.getLogger(get_logger_name())
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(levelname)-8s - %(name)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

debug_handler = logging.StreamHandler()
debug_handler.setLevel(logging.DEBUG)
debug_handler.setFormatter(formatter)
logger.addHandler(debug_handler)

error_handler = logging.handlers.RotatingFileHandler('{dir}/error.log'.format(dir=_LOG_DIR), maxBytes=1024*10, backupCount=3)
error_handler.setLevel(logging.ERROR)
error_handler.setFormatter(formatter)
logger.addHandler(error_handler)

general_file_handler = logging.handlers.RotatingFileHandler('{dir}/app.log'.format(dir=_LOG_DIR), maxBytes=1024*10, backupCount=3)
general_file_handler.setLevel(logging.INFO)
general_file_handler.setFormatter(formatter)
logger.addHandler(general_file_handler)
