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
import datetime
import json

from flask import abort
from flask_restx import fields, Resource, reqparse, inputs
from flask_security import http_auth_required, current_user, AnonymousUser

from .base import api
from .cohort import cohort_get
from .subject import subject_get
from .experiment import experiment_get
from .external_objects import external_systems
from .summary_models import callback_summary, callback_execution_summary, state_summary
from .action import action_get

from ... import exceptions, models
from ...control import update_state, update_callback_execution_state
from ...util.helpers import http_auth_optional

db = models.db

callback_list = api.model('CallbackList', {
    'callbacks': fields.List(fields.Nested(callback_summary))
})


callback_get = api.model('CallbackGet', {
    'uri': fields.Url('api_v2.callback'),
    'state': fields.Nested(state_summary),
    'label': fields.String,
    'executions': fields.List(fields.Nested(callback_execution_summary)),
    'function': fields.String,
    'callback_arguments': fields.String,
    'run_timeout': fields.Integer,
    'wait_timeout': fields.Integer,
    'initial_delay': fields.Integer,
    'description': fields.String,
    'condition': fields.String,
})


callback_put = api.model('CallbackPut', {
    'label': fields.String,
    'function': fields.String,
    'callback_arguments': fields.String,
    'run_timeout': fields.Integer,
    'wait_timeout': fields.Integer,
    'initial_delay': fields.Integer,
    'description': fields.String,
    'condition': fields.String,
})


@api.route('/callbacks', endpoint='callbacks')
class CallbackListAPI(Resource):
    @http_auth_required
    @api.marshal_with(callback_list)
    @api.response(200, 'Success')
    def get(self):
        callbacks = models.Callback.query.order_by(models.Callback.id).all()
        return {"callbacks": callbacks}


@api.route('/callbacks/<int:id>', endpoint='callback')
class CallbackAPI(Resource):
    request_parser = reqparse.RequestParser()
    request_parser.add_argument('label', type=str, required=False, location='json')
    request_parser.add_argument('function', type=str, required=False, location='json')
    request_parser.add_argument('callback_arguments', type=str, required=False, location='json')
    request_parser.add_argument('run_timeout', type=int, required=False, location='json')
    request_parser.add_argument('wait_timeout', type=int, required=False, location='json')
    request_parser.add_argument('initial_delay', type=int, required=False, location='json')
    request_parser.add_argument('description', type=str, required=False, location='json')
    request_parser.add_argument('condition', type=str, required=False, location='json')

    # Request parser for the get function when filtering
    @http_auth_required
    @api.marshal_with(callback_get)
    @api.response(200, 'Success')
    @api.response(404, 'Could not find specified callback')
    def get(self, id):
        callback = models.Callback.query.filter(models.Callback.id == id).one_or_none()
        if callback is None:
            abort(404)
        return callback

    @http_auth_required
    @api.marshal_with(callback_get)
    @api.expect(callback_put)
    @api.response(200, 'Success')
    @api.response(404, 'Could not find callback')
    def put(self, id: int):
        callback = models.Callback.query.filter(models.Callback.id == id).one_or_none()
        if callback is None:
            abort(404)
        
        args = self.request_parser.parse_args()

        if 'label' in args:
            callback.label = args['label']

        if 'function' in args:
            callback.function = args['function']

        if 'callback_arguments' in args:
            callback.callback_arguments = args['callback_arguments']

        if 'run_timeout' in args:
            callback.run_timeout = args['run_timeout']

        if 'wait_timeout' in args:
            callback.wait_timeout = args['wait_timeout']

        if 'initial_delay' in args:
            callback.initial_delay = args['initial_delay']

        if 'description' in args:
            callback.description = args['description']

        if 'condition' in args:
            callback.condition = args['condition']

        db.session.commit()
        db.session.refresh(callback)

        return callback


callback_execution_get = api.model('CallbackExecutionGet', {
    'id': fields.Integer,
    'uri': fields.Url('api_v2.callback_execution'),
    'api_uri': fields.String,
    'web_uri': fields.String,
    'callback': fields.Nested(callback_get),
    'cohort': fields.Nested(cohort_get),
    'subject': fields.Nested(subject_get),
    'experiment': fields.Nested(experiment_get),
    'action': fields.Nested(action_get),
    'external_systems': fields.Raw,
    'status': fields.String,
    'result': fields.String,
    'run_log': fields.String,
    'result_log': fields.String,
    'result_values': fields.Raw,
    'created': fields.DateTime,
    'run_start': fields.DateTime,
    'wait_start': fields.DateTime,
    'finished': fields.DateTime,
})


callback_execution_put = api.model('CallbackExecutionPut', {
    'status': fields.String,
    'result': fields.String,
    'run_log': fields.String,
    'result_log': fields.String,
    'result_values': fields.Raw,
})


@api.route('/callback_executions/<int:id>', endpoint='callback_execution')
class CallbackExecutionAPI(Resource):
    get_parser = reqparse.RequestParser()
    get_parser.add_argument('secret_key', type=str, required=False, location='json')

    request_parser = reqparse.RequestParser()
    request_parser.add_argument('secret_key', type=str, required=False, location='json')
    request_parser.add_argument('status', type=str, required=False, location='json',
                                choices=[x.name for x in models.CallbackExecutionStatus])
    request_parser.add_argument('result', type=str, required=False, location='json',
                                choices=[x.name for x in models.CallbackExecutionResult])
    request_parser.add_argument('run_log', type=str, required=False, location='json')
    request_parser.add_argument('result_log', type=str, required=False, location='json')
    request_parser.add_argument('result_values', type=dict, required=False, location='json')

    @http_auth_optional
    @api.marshal_with(callback_execution_get)
    @api.response(200, 'Success')
    @api.response(404, 'Could not find specified callback_execution execution')
    def get(self, id):
        callback_execution = models.CallbackExecution.query.filter(models.CallbackExecution.id == id).one_or_none()
        if callback_execution is None:
            abort(404)
        
        args = self.get_parser.parse_args()

        # Check if either permission or secret key is correct
        if not ((current_user.is_authenticated and current_user.has_permission('action_update'))
                or callback_execution.secret_key == args.get('secret_key')):
            abort(403, 'Cannot access specified callback_execution')

        return callback_execution

    @http_auth_optional
    @api.marshal_with(callback_execution_get)
    @api.expect(callback_execution_put)
    @api.response(200, 'Success')
    @api.response(404, 'Could not find callback_execution')
    def put(self, id: int):
        # TODO: do we feel there is a security risk because of the order of permissions?
        # you can see if an execution exists or not by checking error status
        callback_execution = models.CallbackExecution.query.filter(models.CallbackExecution.id == id).one_or_none()
        if callback_execution is None:
            abort(404)
        
        args = self.request_parser.parse_args()
        secret_key_arg = args.get('secret_key')

        # Check if either the user is authenticated and has permission OR that there is a valid secret key and it is
        # matching. We need to check authenticated first because anonymous users don't have the has_permission
        if not ((current_user.is_authenticated and current_user.has_permission('action_update'))
                or (secret_key_arg and callback_execution.secret_key == secret_key_arg)):
            abort(403, 'Cannot access specified callback_execution')

        # Executions can't be updated once they are finished!
        if callback_execution.status.resolved or callback_execution.finished:
            abort(409)

        # Save previous state and current state info for checking if state update needs to be triggered
        previously_finished = callback_execution.status.resolved
        if args.get('result') is not None:
            # The the argument and construct the correct enum
            result = args['result']
            result = models.CallbackExecutionResult[result]
            callback_execution.result = result

        if args.get('run_log') is not None:
            callback_execution.run_log = args['run_log']

        if args.get('result_log') is not None:
            callback_execution.result_log = args['result_log']

        if args.get('result_values') is not None:
            callback_execution.result_values = json.dumps(args['result_values'], indent=2)

        status = args.get('status')
        if status is not None:
            update_callback_execution_state(callback_execution, status)

        db.session.commit()
        db.session.refresh(callback_execution)

        # Check if the state needs updating
        if status is not None and callback_execution.status.resolved and not previously_finished:
            update_state(callback_execution.action.experiment)

        return callback_execution



