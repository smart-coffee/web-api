import json

from typing import List

from flasgger import swag_from
from flask import Blueprint
from flask_restful import Api, marshal_with, Resource

from controllers.job import JobController
from models import User, Job
from controllers.response_model import get_job_fields
from utils.http import token_required, get_post_response, serialize


API_PREFIX = 'job'
JOB_BP = Blueprint('{rsc}_api'.format(rsc=API_PREFIX), __name__)
api = Api(JOB_BP)


class JobListResource(Resource):
    def __init__(self):
        self.controller = JobController()
    
    @token_required(roles=['Administrator'])
    @swag_from('/resources/jobs/description/jobs_list_get.yml')
    @marshal_with(get_job_fields())
    def get(self, current_user: User) -> List[Job]:
        return self.controller.get_list(current_user)
    
    @token_required(roles=['Administrator'])
    @swag_from('/resources/jobs/description/jobs_list_post.yml')
    def post(self, current_user: User) -> Job:
        job = self.controller.create(current_user)
        serialized_job = serialize(job, get_job_fields())
        json_job = json.dumps(serialized_job)
        response = get_post_response(obj=job, body=json_job, content_type='application/json', api='/{rsc}'.format(rsc=API_PREFIX))
        return response


api.add_resource(JobListResource, '/{rsc}'.format(rsc=API_PREFIX))
