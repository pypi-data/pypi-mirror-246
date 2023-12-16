# Copyright 2017-2021 Biomedical Imaging Group Rotterdam, Departments of
# Medical Informatics and Radiology, Erasmus MC, Rotterdam, The Netherlands
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import yaml

from flask import abort
from flask_restx import fields, Resource, reqparse
from flask_security import http_auth_required, roles_accepted

from .base import api
from .summary_models import workflow_summary
from ... import models
from ...util.periodic_tasks import check_timeouts
from ...util.helpers import create_workflow

db = models.db

check_timeouts_post = api.model('CheckTimeoutsPost', {
    'run_timeouts': fields.Integer,
    'wait_timeouts': fields.Integer,
})


@api.route('/service/check_timeouts', endpoint='check_timeouts')
class CheckTimeoutApi(Resource):
    @http_auth_required
    @api.marshal_with(check_timeouts_post)
    @api.response(200, 'Success')
    def post(self):
        run_timeouts, wait_timeouts = check_timeouts()

        return {
            'run_timeouts': run_timeouts,
            'wait_timeouts': wait_timeouts,
        }

@api.route('/service/config/import-workflow', endpoint='import-workflow')
class WorkflowImportAPI(Resource):
    post_request_parser = reqparse.RequestParser()
    post_request_parser.add_argument('workflow_definition',
                                        type=str,
                                        required=True,
                                        location='json',
                                        help='No label specified')
    
    @http_auth_required
    @roles_accepted('admin')
    @api.expect(post_request_parser)
    @api.marshal_with(workflow_summary)
    @api.response(201, 'Created')
    def post(self):
        args = self.post_request_parser.parse_args()
        workflow_definition = args.get('workflow_definition')
        
        try:
            workflow_definition = yaml.safe_load(workflow_definition)
            workflow_label = workflow_definition['label']
        except yaml.YAMLError as exc:
            abort(400, f'Workflow definition is not a valid YAML file. {exc}')
        except KeyError:
            abort(400, 'Workflow definition should contain a label to manage multiple versions')
        workflow = models.Workflow.query.filter(models.Workflow.label == workflow_label).one_or_none()
        
        if workflow is None:
            try:
                workflow = create_workflow(workflow_definition)
                db.session.commit()
                return workflow, 201
            except:
                abort(400, 'Workflow definition is invalid.')
        else:
            abort(409, f'Workflow {workflow_label} already exists.')
            