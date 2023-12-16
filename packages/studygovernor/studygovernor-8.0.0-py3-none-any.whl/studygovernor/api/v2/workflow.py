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
from flask_security import http_auth_required


from .base import api
from .state import state_list, state_model
from .summary_models import workflow_summary
from ... import models
from ...util.helpers import create_workflow, upgrade_workflow

db = models.db


workflow_list = api.model('WorkflowList', {
    'workflows': fields.List(fields.Nested(workflow_summary))
})


@api.route('/workflows', endpoint='workflows')
class WorkflowListAPI(Resource):
    post_request_parser = reqparse.RequestParser()
    post_request_parser.add_argument('workflow_definition',
                                        type=str,
                                        required=True,
                                        location='json',
                                        help='No label specified')
    
    @http_auth_required
    @api.marshal_with(workflow_list)
    @api.response(200, 'Success')
    def get(self):
        workflows = models.Workflow.query.order_by(models.Workflow.id).all()
        return {'workflows': workflows}

@api.route('/workflows/<int:id>', endpoint='workflow')
class WorkflowAPI(Resource):
    put_request_parser = reqparse.RequestParser()
    put_request_parser.add_argument('workflow_definition',
                                        type=str,
                                        required=True,
                                        location='json',
                                        help='No label specified')
    
    @http_auth_required
    @api.marshal_with(workflow_summary)
    @api.response(200, 'Success')
    @api.response(404, 'Could not find specified workflow')
    def get(self, id):
        workflow = models.Workflow.query.filter(models.Workflow.id == id).one_or_none()
        if workflow is None:
            abort(404)
        return workflow


@api.route('/workflows/by-label/<label>', endpoint='workflow_by_label')
class WorkflowByLabelAPI(Resource):
    @http_auth_required
    @api.marshal_with(workflow_summary)
    @api.response(200, 'Success')
    @api.response(404, 'Could not find specified workflow')
    def get(self, label):
        workflow = models.Workflow.query.filter(models.Workflow.label == label).one_or_none()
        if workflow is None:
            abort(404)
        return workflow


@api.route('/workflows/<workflow_label>/states', endpoint='workflow_states')
class WorkflowStateListAPI(Resource):
    @http_auth_required
    @api.marshal_with(state_list)
    @api.response(200, 'Success')
    def get(self, workflow_label):
        workflow = models.Workflow.query.filter(models.Workflow.label == workflow_label).one_or_none()
        if workflow is None:
            abort(404)
        return {'states': workflow.states}


@api.route('/workflows/<workflow_label>/states/<state_label>', endpoint='workflow_state')
class WorkflowStateAPI(Resource):
    @http_auth_required
    @api.marshal_with(state_model)
    @api.response(200, 'Success')
    @api.response(404, 'Could not find specified state')
    def get(self, workflow_label, state_label):
        state = models.State.query.filter((models.State.workflow.has(label=workflow_label)) & (models.State.label == state_label)).one_or_none()
        if state is None:
            abort(404)
        return state
