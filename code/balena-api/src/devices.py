import json

from flask import Blueprint
from balena import Balena

get_devices_api = Blueprint('get_devices', __name__)
balena = Balena()

@get_devices_api.route('/<application>/devices', methods=['GET'])
def get_devices(application):
    devices = balena.models.device.get_all_by_application(application)
    return json.dumps(devices)
    