from flask import redirect, Blueprint
from config.environment_tools import get_swagger_base_url


def get_swagger_spec():
    return {
        "title": "TTC RESTful API Spec",
        "version": "1.0.0",
        # "headers": [
        #     ('Access-Control-Allow-Origin', '*'),
        #     ('Access-Control-Allow-Methods', "GET, POST, PUT, DELETE, OPTIONS"),
        #     ('Access-Control-Allow-Credentials', "true"),
        # ],
        "contact": {
            "responsibleOrganization": "TTC Sülzfeld 08 e.V.",
            "responsibleDeveloper": "Tobias Blaufuß",
            "email": "tobias.blaufuss@outlook.de",
            "url": "https://www.tobias-blaufuss.de",
        },
        "specs": [
            {
                "endpoint": 'ttc_apispec',
                "route": '/ttc_apispec.json',
                "rule_filter": lambda rule: True,  # all in
                "model_filter": lambda tag: True,  # all in
            }
        ],
        "specs_route": "/apidocs"
    }


def get_swagger_template():
    return {
      #"swagger": "2.0",
      #"info": {
        #"title": "My API",
        #"description": "API for my data",
        #"contact": {
        #  "responsibleOrganization": "ME",
        #  "responsibleDeveloper": "Me",
        #  "email": "me@me.com",
        #  "url": "www.me.com",
        #},
        #"termsOfService": "http://me.com/terms",
        #"version": "0.0.1"
      #},"hello"
      #"host": "mysite.com",  # overrides localhost:500
      "basePath": get_swagger_base_url(),  # base bash for blueprint registration
      "schemes": [
        "https",
        "http"
      ]
    }


INDEX_SWAGGER_BP = Blueprint('index_swagger_api', __name__)


@INDEX_SWAGGER_BP.route('/')
def index():
    spec = get_swagger_spec()
    path = spec['specs_route']
    return redirect(path, code=302)
