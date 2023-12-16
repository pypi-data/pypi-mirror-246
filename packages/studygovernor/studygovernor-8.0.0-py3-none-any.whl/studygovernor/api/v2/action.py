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

from flask import abort
from flask_restx import fields, Resource, reqparse, inputs
from flask_security import http_auth_required, permissions_accepted

from .base import api
from .summary_models import action_summary, callback_execution_summary, experiment_summary, transition_summary

from ... import models


db = models.db


action_list = api.model('ActionList', {
    'actions': fields.List(fields.Nested(action_summary))
})


@api.route('/actions', endpoint='actions')
class ActionListAPI(Resource):
    @http_auth_required
    @api.marshal_with(action_list)
    @api.response(200, 'Success')
    def get(self):
        actions = models.Action.query.order_by(models.Action.id).all()
        return {'actions': actions}


action_get = api.model('ActionGet', {
    'id': fields.Integer,
    'uri': fields.Url('api_v2.action'),
    'api_uri': fields.String,
    'web_uri': fields.String,
    'experiment': fields.Nested(experiment_summary),
    'transition': fields.Nested(transition_summary),
    'executions': fields.List(fields.Nested(callback_execution_summary)),
    'success': fields.Boolean,
    'return_value': fields.String,
    'freetext': fields.String,
    'start_time': fields.DateTime(dt_format='iso8601'),
    'end_time': fields.DateTime(dt_format='iso8601'),
})


action_put = api.model('ActionPut', {
    'success': fields.Boolean,
    'return_value': fields.String,
    'end_time': fields.DateTime(dt_format='iso8601'),
})


@api.route('/actions/<int:id>', endpoint='action')
class ActionAPI(Resource):
    request_parser = reqparse.RequestParser()
    request_parser.add_argument('success', type=bool, required=False, location='json')
    request_parser.add_argument('return_value', type=str, required=False, location='json')
    request_parser.add_argument('end_time', type=inputs.datetime_from_iso8601, required=False, location='json')

    @http_auth_required
    @api.marshal_with(action_get)
    @api.response(200, 'Success')
    @api.response(404, 'Could not find action')
    def get(self, id: int):
        action = models.Action.query.filter(models.Action.id == id).one_or_none()
        if action is None:
            abort(404)
        return action

    @http_auth_required
    @permissions_accepted('action_update')
    @api.marshal_with(action_get)
    @api.expect(action_put)
    @api.response(200, 'Success')
    @api.response(404, 'Could not find action')
    def put(self, id: int):
        action = models.Action.query.filter(models.Action.id == id).one_or_none()
        if action is None:
            abort(404)

        args = self.request_parser.parse_args()

        if 'success' in args:
            action.success = args['success']

        if 'return_value' in args:
            action.return_value = args['return_value']

        if 'end_time' in args:
            action.end_time = args['end_time']

        db.session.commit()
        db.session.refresh(action)

        return action
