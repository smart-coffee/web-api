import json

from typing import List
from flasgger import swag_from
from flask import Blueprint
from flask_restful import Api, marshal_with, Resource

from controllers.user import CurrentUserController, PublicUserController, CurrentUserProfileController
from controllers.job import CurrentUserJobController
from models import User, Profile, Job
from controllers.response_model import get_registered_user_details, get_profile_fields, get_job_fields
from utils.http import token_required, get_post_response, get_delete_response, serialize


API_PREFIX = 'users'
USER_BP = Blueprint('{rsc}_api'.format(rsc=API_PREFIX), __name__)
api = Api(USER_BP)


class CurrentUserResource(Resource):
    def __init__(self):
        self.controller = CurrentUserController()

    @token_required()
    @swag_from('/resources/users/description/current_user_get.yml')
    @marshal_with(get_registered_user_details())
    def get(self, current_user: User):
        return current_user

    @token_required()
    @swag_from('/resources/users/description/current_user_put.yml')
    @marshal_with(get_registered_user_details())
    def put(self, current_user: User):
        return self.controller.edit(resource_id=current_user.get_id(), current_user=current_user)


class CurrentUserProfileListResource(Resource):
    def __init__(self):
        self.controller = CurrentUserProfileController()

    @token_required()
    @swag_from('/resources/users/description/current_user_profile_list_get.yml')
    @marshal_with(get_profile_fields())
    def get(self, current_user: User) -> List[Profile]:
        return self.controller.get_list(current_user)

    @token_required()
    @swag_from('/resources/users/description/current_user_profile_list_post.yml')
    def post(self, current_user: User) -> Profile:
        profile = self.controller.create(current_user)
        serialized_profile = serialize(profile, get_profile_fields())
        json_profile = json.dumps(serialized_profile)
        response = get_post_response(obj=profile, body=json_profile, content_type='application/json', api='/{rsc}/current/profiles'.format(rsc=API_PREFIX))
        return response


class CurrentUserProfileResource(Resource):
    def __init__(self):
        self.controller = CurrentUserProfileController()

    @token_required()
    @swag_from('/resources/users/description/current_user_profile_get.yml')
    @marshal_with(get_profile_fields())
    def get(self, profile_id, current_user: User) -> Profile:
        return self.controller.get_by_id(profile_id, current_user)

    @token_required()
    @swag_from('/resources/users/description/current_user_profile_put.yml')
    @marshal_with(get_profile_fields())
    def put(self, profile_id, current_user: User) -> Profile:
        return self.controller.edit(resource_id=profile_id, current_user=current_user)

    @token_required()
    @swag_from('/resources/users/description/current_user_profile_delete.yml')
    def delete(self, profile_id, current_user: User):
        self.controller.delete(resource_id=profile_id, current_user=current_user)
        return get_delete_response()
        

class PublicUserResource(Resource):
    def __init__(self):
        self.controller = PublicUserController()
    
    @swag_from('/resources/users/description/public_user_post.yml')
    # Marshal will not work because of 'Response' object
    #@marshal_with(get_registered_user_details())
    def post(self):
        new_user = self.controller.create()
        serialized_user = serialize(new_user, get_registered_user_details())
        json_user = json.dumps(serialized_user)
        response = get_post_response(obj=new_user, body=json_user, content_type='application/json', api='/public/{rsc}'.format(rsc=API_PREFIX))
        return response


class CurrentUserJobListResource(Resource):
    def __init__(self):
        self.controller = CurrentUserJobController()
    
    @token_required()
    @swag_from('/resources/users/description/current_user_jobs_list_get.yml')
    @marshal_with(get_job_fields())
    def get(self, current_user: User) -> List[Job]:
        return self.controller.get_list(current_user)

    @token_required()
    @swag_from('/resources/users/description/current_user_jobs_list_post.yml')
    def post(self, current_user: User) -> Job:
        job = self.controller.create(current_user)
        serialized_job = serialize(job, get_job_fields())
        json_job = json.dumps(serialized_job)
        response = get_post_response(obj=job, body=json_job, content_type='application/json', api='/{rsc}/current/jobs'.format(rsc=API_PREFIX))
        return response


api.add_resource(CurrentUserResource, '/{rsc}/current'.format(rsc=API_PREFIX))
api.add_resource(PublicUserResource, '/public/{rsc}'.format(rsc=API_PREFIX))
api.add_resource(CurrentUserProfileListResource, '/{rsc}/current/profiles'.format(rsc=API_PREFIX))
api.add_resource(CurrentUserProfileResource, '/{rsc}/current/profiles/<int:profile_id>'.format(rsc=API_PREFIX))
api.add_resource(CurrentUserJobListResource, '/{rsc}/current/jobs'.format(rsc=API_PREFIX))
