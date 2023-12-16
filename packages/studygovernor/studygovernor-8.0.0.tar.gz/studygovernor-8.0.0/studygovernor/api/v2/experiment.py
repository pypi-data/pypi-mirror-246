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
from flask_security import http_auth_required, permissions_required

from .action import action_list
from .base import api
from .summary_models import experiment_summary, state_summary, subject_summary, workflow_summary
from ... import control, exceptions, models
from ...fields import MappingField

db = models.db


experiment_list = api.model('ExperimentList', {
    'experiments': fields.List(fields.Nested(experiment_summary))
})


experiment_get = api.model('ExperimentGet', {
    'id': fields.Integer,
    'label': fields.String,
    'uri': fields.Url('api_v2.experiment'),
    'api_uri': fields.String,
    'web_uri': fields.String,
    'subject': fields.Nested(subject_summary),
    'scandate': fields.DateTime(dt_format='iso8601'),
    'state': fields.Nested(state_summary),
    'external_ids': MappingField,
    'variable_map': fields.Raw,
})


@api.route('/experiments', endpoint='experiments')
class ExperimentListAPI(Resource):
    # Request parser for the get function when filtering
    get_request_parser = reqparse.RequestParser()
    get_request_parser.add_argument('scandate', type=inputs.datetime_from_iso8601, required=False,
                                    location='args')
    get_request_parser.add_argument('subject_id', type=str, required=False,
                                    location='args')
    get_request_parser.add_argument('state', type=str, required=False,
                                    location='args')
    get_request_parser.add_argument('offset', type=int, required=False,
                                    location='args', help="Offset for pagination")
    get_request_parser.add_argument('limit', type=int, required=False,
                                    location='args', help="Maximum number of rows returned")

    # Request parser for when adding an experiment
    post_request_parser = reqparse.RequestParser()
    post_request_parser.add_argument('label', type=str, required=True, location='json',
                                     help='No label supplied')
    post_request_parser.add_argument('scandate', type=inputs.datetime_from_iso8601, required=True,
                                     location='json', help='No scandate supplied')
    post_request_parser.add_argument('subject_id', type=int, required=True, location='json',
                                     help='No subject supplied')
    post_request_parser.add_argument('workflow_label', type=str, required=False, location='json')

    @http_auth_required
    @api.expect(get_request_parser)
    @api.marshal_with(experiment_list)
    @api.response(200, 'Success')
    def get(self):
        args = self.get_request_parser.parse_args()
        offset = args['offset']
        limit = args['limit']

        experiments, count = control.get_experiments(
            scandate=args['scandate'],
            subject=args['subject_id'],
            state=args['state'],
            offset=offset,
            limit=limit,
        )

        return {
            'experiments': experiments,
            'offset': offset,
            'limit': limit,
            'count': count,
        }

    @http_auth_required
    @permissions_required('sample_add')
    @api.marshal_with(experiment_get)
    @api.expect(post_request_parser)
    @api.response(201, 'Created experiment')
    @api.response(404, 'Could not find specified subject or workflow')
    def post(self):
        args = self.post_request_parser.parse_args()

        # Find the id for the subject, allow selection of the filter field ID or label (or auto detect)
        subject = models.Subject.query.filter(models.Subject.id == args['subject_id']).one_or_none()
        if subject is None:
            abort(404)

        if args.get('workflow_label') is not None:
            workflow = models.Workflow.query.filter(models.Workflow.label == args['workflow_label']).one_or_none()
            if workflow is None:
                abort(404)
        else:
            workflow = models.Workflow.query.order_by(models.Workflow.id.desc()).first()

        # Post the experiment
        print(f'[DEBUG] Creating experiment {args["label"]}')
        print(f'[DEBUG] Found subject to be {subject}')
        experiment = control.create_experiment(workflow, label=args['label'], scandate=args['scandate'], subject=subject)
        db.session.add(experiment)
        db.session.commit()
        db.session.refresh(experiment)
        print('[DEBUG] EXPERIMENT: {}'.format(experiment.id))

        return experiment, 201


@api.route('/experiments/<int:id>', endpoint='experiment')
class ExperimentAPI(Resource):
    
    @http_auth_required
    @api.marshal_with(experiment_get)
    @api.response(200, 'Success')
    @api.response(404, 'Could not find experiment')
    def get(self, id):
        experiment = models.Experiment.query.filter(models.Experiment.id == id).one_or_none()
        if experiment is None:
            abort(404)
        return experiment
        

experiment_state_model = api.model('ExperimentState', {
    'state': fields.Nested(state_summary),
})


experiment_state_put = api.model('StatePut', {
    'state': fields.Nested(state_summary),
    'error': fields.Raw,
    'success': fields.Boolean,
})


@api.route('/experiments/<int:id>/actions', endpoint='experiment_actions')
class ActionListAPI(Resource):
    @http_auth_required
    @api.marshal_with(action_list)
    @api.response(200, 'Success')
    def get(self, id: int):
        actions = models.Action.query.filter(models.Action.experiment_id == id).order_by(models.Action.id).all()
        return {'actions': actions}


@api.route('/experiments/<int:id>/state', endpoint='experiment_state')
class ExperimentStateAPI(Resource):
    request_parser = reqparse.RequestParser()
    request_parser.add_argument('state_label', type=str, required=True, location='json',
                                help='No state supplied')
    request_parser.add_argument('freetext', type=str, required=False, location='json',
                                help='Free text annotation for the created action')

    @http_auth_required
    @api.marshal_with(experiment_state_model)
    @api.response(200, 'Success')
    @api.response(404, 'Could not find specified experiment')
    def get(self, id):
        experiment = models.Experiment.query.filter(models.Experiment.id == id).one_or_none()
        if experiment is None:
            abort(404)
        return {"state": experiment.state}

    @http_auth_required
    @permissions_required('sample_state_update')
    @api.marshal_with(experiment_state_put)
    @api.expect(request_parser)
    @api.response(200, 'Success')
    @api.response(404, 'Could not find specified state')
    @api.response(409, 'Cannot change state to specified state, no valid transition!')
    def put(self, id):
        experiment = models.Experiment.query.filter(models.Experiment.id == id).one_or_none()
        if experiment is None:
            abort(404)
        
        current_workflow = experiment.state.workflow

        args = self.request_parser.parse_args()
        
        state = models.State.query.filter((models.State.workflow==current_workflow) & (models.State.label==args['state_label'])).one_or_none()

        if state is None:
            success = False
            error = {
                'errorclass': 'StateNotFoundError',
                'requested_state': args['state_label'],
                'message': 'Could not find requested state "{}"'.format(args['state_label']),
            }
            status = 404
        else:
            # Try to change the state
            try:
                control.set_state(experiment, state, 'api_v2', args['freetext'])
                success = True
                error = None
                status = 200
            except exceptions.StateChangeError as err:
                success = False
                error = err.marshal(api_prefix='api_v2')
                status = 409

        data = {
            'state': experiment.state,
            'error': error,
            'success': success,
        }

        return data, status


experiment_external_ids_get = api.model('ExperimentExternalIdsGet', {
    'experiment_id': fields.Integer,
    'experiment_label': fields.String,
    'external_ids': MappingField
})

@api.route('/experiments/<int:id>/external_ids', endpoint='experiment_external_ids')
class ExperimentExternalIdsAPI(Resource):
    post_request_parser = reqparse.RequestParser()
    post_request_parser.add_argument('external_ids', type=dict, required=True, location='json',
                                help='No external ids supplied')
    
    @http_auth_required
    @api.marshal_with(experiment_external_ids_get)
    @api.response(200, 'Success')
    @api.response(404, 'Could not find specified experiment')
    def get(self, id):
        experiment = models.Experiment.query.filter(models.Experiment.id == id).one_or_none()
        if experiment is None:
            abort(404)
        return {
            'experiment_id': experiment.id,
            'experiment_label': experiment.label,
            'external_ids': experiment.external_ids
        }

    @http_auth_required
    @permissions_required('sample_update')
    @api.expect(post_request_parser)
    @api.marshal_with(experiment_external_ids_get)
    @api.response(201, 'Added external ids')
    @api.response(404, 'Could not find specified experiment or external system')
    def post(self,id):
        args = self.post_request_parser.parse_args()
        external_ids = args['external_ids']

        experiment = models.Experiment.query.filter(models.Experiment.id == id).one_or_none()
        if experiment is None:
            abort(404)
        
        for system_name, external_id in external_ids.items():
            external_system = models.ExternalSystem.query.filter(models.ExternalSystem.system_name == system_name).one_or_none()
            if external_system is None:
                abort(404)
            external_experiment_link = models.ExternalExperimentLinks.query.filter_by(experiment=experiment, external_system=external_system).one_or_none()
        
            # Create link if it doesn't exist
            if external_experiment_link is None:
                external_experiment_link = models.ExternalExperimentLinks(external_id=external_id, experiment=experiment, external_system=external_system)
                db.session.add(external_experiment_link)
            else:
                external_experiment_link.external_id = external_id

        db.session.commit()
        
        return {
            'experiment_id': experiment.id,
            'experiment_label': experiment.label,
            'external_ids': experiment.external_ids
        }, 201


@api.route('/experiments/<int:id>/external_ids/<system_name>', endpoint='experiment_system_external_id')
class ExperimentExternalSystemIdAPI(Resource):
    put_request_parser = reqparse.RequestParser()
    put_request_parser.add_argument('external_id', type=str, required=True, location='json',
                                help='No external ids supplied')
    
    
    @http_auth_required
    @permissions_required('sample_update')
    @api.expect(put_request_parser)
    @api.marshal_with(experiment_external_ids_get)
    @api.response(201, 'Changed external id')
    @api.response(404, 'Could not find specified experiment or external system')
    def put(self, id, system_name):
        args = self.put_request_parser.parse_args()
        external_id = args['external_id']

        experiment = models.Experiment.query.filter(models.Experiment.id == id).one_or_none()
        external_system = models.ExternalSystem.query.filter(models.ExternalSystem.system_name == system_name).one_or_none()
        
        if experiment is None or external_system is None:
            abort(404)
        
        external_experiment_link = models.ExternalExperimentLinks.query.filter_by(experiment=experiment, external_system=external_system).one_or_none()
    
        # Create link if it doesn't exist
        if external_experiment_link is None:
            external_experiment_link = models.ExternalExperimentLinks(external_id=external_id, experiment=experiment, external_system=external_system)
            db.session.add(external_experiment_link)
        else:
            external_experiment_link.external_id = external_id

        db.session.commit()
        
        return {
            'experiment_id': experiment.id,
            'experiment_label': experiment.label,
            'external_ids': experiment.external_ids
        }, 201

    @http_auth_required
    @permissions_required('sample_delete')
    @api.marshal_with(experiment_external_ids_get)
    @api.response(200, 'Success')
    @api.response(404, 'Could not find specified experiment, external system or external id')
    def delete(self, id, system_name):
        
        experiment = models.Experiment.query.filter(models.Experiment.id == id).one_or_none()
        external_system = models.ExternalSystem.query.filter(models.ExternalSystem.system_name == system_name).one_or_none()
        
        if experiment is None or external_system is None:
            abort(404)
        
        external_experiment_link = models.ExternalExperimentLinks.query.filter_by(experiment=experiment, external_system=external_system).one_or_none()
    
        # Delete link if it exists
        if external_experiment_link is None:
            abort(404)
        else:
            db.session.delete(external_experiment_link)

        db.session.commit()
        
        return {
            'experiment_id': experiment.id,
            'experiment_label': experiment.label,
            'external_ids': experiment.external_ids
        }

