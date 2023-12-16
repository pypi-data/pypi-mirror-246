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
from flask_restx import fields, Resource, reqparse
from flask_security import http_auth_required, permissions_accepted
from sqlalchemy.exc import IntegrityError


from .base import api
from .summary_models import experiment_summary, subject_summary
from ... import models

db = models.db

external_system_model = api.model('ExternalSystem', {
    'id': fields.Integer,
    'uri': fields.Url('api_v2.external_system'),
    'url': fields.String,
    'system_name': fields.String,
})

external_systems = api.model('ExternalSystems', {
    'external_systems': fields.List(fields.Nested(external_system_model))
})

@api.route('/external_systems', endpoint='external_systems')
class ExternalSystemListAPI(Resource):
    @http_auth_required
    @api.marshal_with(external_systems)
    @api.response(200, 'Success')
    def get(self):
        external_systems = models.ExternalSystem.query.order_by(models.ExternalSystem.id).all()
        return {'external_systems': external_systems}
    

@api.route('/external_systems/<int:id>', endpoint='external_system')
class ExternalSystemAPI(Resource):
    @http_auth_required
    @api.marshal_with(external_system_model)
    @api.response(200, 'Success')
    @api.response(404, 'Cannot find specified external system')
    def get(self, id):
        external_system = models.ExternalSystem.query.filter(models.ExternalSystem.id == id).one_or_none()

        if external_system is None:
            abort(404)
        return external_system


@api.route('/external_systems/by-name/<system_name>', endpoint='external_system_by_name')
class ExternalSystemAPI(Resource):
    @http_auth_required
    @api.marshal_with(external_system_model)
    @api.response(200, 'Success')
    @api.response(404, 'Cannot find specified external system')
    def get(self, system_name):
        external_system = models.ExternalSystem.query.filter(models.ExternalSystem.system_name == system_name).one_or_none()

        if external_system is None:
            abort(404)
        return external_system


external_subject = api.model('ExternalSubjectLinksGet', {
    'id': fields.Integer,
    'uri': fields.Url('api_v2.external_subject_link'),
    'subject': fields.Nested(subject_summary),
    'external_system': fields.Nested(external_system_model),
    'external_id': fields.String,
})

external_subject_links = api.model('ExternalSubjectLinks', {
    'external_subject_links': fields.List(fields.Nested(external_subject))
})


external_subject_links_post = api.model('ExternalSubjectLinksPost', {
    'subject_id': fields.Integer,
    'external_system': fields.String,
    'external_id': fields.String,
})


@api.route('/external_subject_links', endpoint='external_subject_links')
class ExternalSubjectListAPI(Resource):
    request_parser = reqparse.RequestParser()
    request_parser.add_argument('subject_id', type=int, required=True, location='json',
                                help='No subject supplied')
    request_parser.add_argument('external_system_name', type=str, required=True, location='json',
                                help='No external system supplied')
    request_parser.add_argument('external_id', type=str, required=True, location='json',
                                help='No external id supplied')

    @http_auth_required
    @api.marshal_with(external_subject_links)
    @api.response(200, 'Success')
    def get(self):
        external_subject_links = models.ExternalSubjectLinks.query.order_by(models.ExternalSubjectLinks.id).all()
        return {'external_subject_links': external_subject_links}

    @http_auth_required
    @permissions_accepted('sample_add')
    @api.marshal_with(external_subject)
    @api.expect(external_subject_links_post)
    @api.response(201, 'Created')
    @api.response(404, 'Specified experiment and/or external system not found')
    @api.response(409, 'External experiment link for subject/external system combination already exists')
    def post(self):
        args = self.request_parser.parse_args()

        subject = models.Subject.query.filter(models.Subject.id == args['subject_id']).one_or_none()
        external_system = models.ExternalSystem.query.filter(models.ExternalSystem.system_name == args['external_system_name']).one_or_none()

        if subject is None or external_system is None:
            abort(404)

        external_subject_link = models.ExternalSubjectLinks(args['external_id'],
                                                            subject=subject,
                                                            external_system=external_system)

        db.session.add(external_subject_link)
        try:
            db.session.commit()
            db.session.refresh(external_subject_link)
        except IntegrityError:
            # This is thrown because of a duplicate external_experiment_link for the same system.
            # Rollback and fetch the original to be returned
            db.session.rollback()
            abort(409)

        return external_subject_link, 201

    @http_auth_required
    @permissions_accepted('sample_add')
    @api.marshal_with(external_subject)
    @api.expect(external_subject_links_post)
    @api.response(201, 'Created')
    @api.response(404, 'Specified experiment and/or external system not found')
    def put(self):
        args = self.request_parser.parse_args()

        subject = models.Subject.query.filter(models.Subject.id==args['subject_id']).one_or_none()
        external_system = models.ExternalSystem.query.filter(models.ExternalSystem.system_name == args['external_system_name']).one_or_none()

        if subject is None or external_system is None:
            abort(404)

        external_subject_link = models.ExternalSubjectLinks.query.filter_by(subject=subject,
                                                                            external_system=external_system).one_or_none()

        # Create link if it doesn't exist
        if external_subject_link is None:
            external_subject_link = models.ExternalSubjectLinks(external_id=args['external_id'],
                                                                subject=subject,
                                                                external_system=external_system)
            db.session.add(external_subject_link)
        else:
            external_subject_link.external_id = args['external_id']

        db.session.commit()
        db.session.refresh(external_subject_link)

        return external_subject_link, 201


@api.route('/external_subject_links/<int:id>', endpoint='external_subject_link')
class ExternalSubjectAPI(Resource):
    @http_auth_required
    @api.marshal_with(external_subject)
    @api.response(200, 'Success')
    @api.response(404, 'Cannot find specified external subject')
    def get(self, id: int):
        external_subject_link = models.ExternalSubjectLinks.query.filter(models.ExternalSubjectLinks.id == id).one_or_none()
        if external_subject_link is None:
            abort(404)
        return external_subject_link


external_experiment = api.model('ExternalExperiment', {
    'id': fields.Integer,
    'uri': fields.Url('api_v2.external_experiment_link'),
    'experiment': fields.Nested(experiment_summary),
    'external_system': fields.Nested(external_system_model),
    'external_id': fields.String,
})

external_experiment_links = api.model('ExternalExperimentLinks', {
    'external_experiment_links': fields.List(fields.Nested(external_experiment))
})

external_experiment_links_post = api.model('ExternalExperimentLinksPost', {
    'experiment': fields.String,
    'external_system': fields.String,
    'external_id': fields.String,
})

external_experiment_links_put = api.model('ExternalExperimentLinksPut', {
    'experiment': fields.String,
    'external_system': fields.String,
    'external_id': fields.String,
})


@api.route('/external_experiment_links', endpoint='external_experiment_links')
class ExternalExperimentListAPI(Resource):
    request_parser = reqparse.RequestParser()
    request_parser.add_argument('experiment_id', type=int, required=True, location='json',
                                help='No experiment supplied')
    request_parser.add_argument('external_system_name', type=str, required=True, location='json',
                                help='No external system supplied')
    request_parser.add_argument('external_id', type=str, required=True, location='json',
                                help='No external id supplied')

    @http_auth_required
    @api.marshal_with(external_experiment_links)
    @api.response(200, 'Success')
    def get(self):
        external_experiment_links = models.ExternalExperimentLinks.query.order_by(models.ExternalExperimentLinks.id).all()
        return {'external_experiment_links': external_experiment_links}

    @http_auth_required
    @permissions_accepted('sample_add')
    @api.marshal_with(external_experiment)
    @api.expect(external_experiment_links_post)
    @api.response(201, 'Created')
    @api.response(404, 'Specified experiment and/or external system not found')
    @api.response(409, 'External experiment link for experiment/external system combination already exists')
    def post(self):
        args = self.request_parser.parse_args()

        # Find the the experiment to link to
        experiment = models.Experiment.query.filter(models.Experiment.id == args['experiment_id']).one_or_none()
        external_system = models.ExternalSystem.query.filter(models.ExternalSystem.system_name == args['external_system_name']).one_or_none()

        if experiment is None or external_system is None:
            abort(404)

        external_experiment_link = models.ExternalExperimentLinks(args['external_id'],
                                                                  experiment=experiment,
                                                                  external_system=external_system)

        db.session.add(external_experiment_link)
        try:
            db.session.commit()
            db.session.refresh(external_experiment_link)
        except IntegrityError:
            # This is thrown because of a duplicate external_system_link for the same system.
            # Rollback and fetch the original to be returned
            db.session.rollback()
            abort(409)

        return external_experiment_link, 201

    @http_auth_required
    @permissions_accepted('sample_add')
    @api.marshal_with(external_experiment)
    @api.expect(external_experiment_links_put)
    @api.response(200, 'Success')
    @api.response(404, 'Specified experiment and/or external system not found')
    def put(self):
        args = self.request_parser.parse_args()

        # Find the the experiment to link to
        experiment = models.Experiment.query.filter(models.Experiment.id==args['experiment_id']).one_or_none()
        external_system = models.ExternalSystem.query.filter(models.ExternalSystem.system_name == args['external_system_name']).one_or_none()

        if experiment is None or external_system is None:
            abort(404)

        external_experiment_link = models.ExternalExperimentLinks.query.filter_by(experiment=experiment, external_system=external_system).one_or_none()
        
        # Create link if it doesn't exist
        if external_experiment_link is None:
            external_experiment_link = models.ExternalExperimentLinks(external_id=args['external_id'], experiment=experiment, external_system=external_system)
            db.session.add(external_experiment_link)
        else:
            external_experiment_link.external_id = args['external_id']

        db.session.commit()
        db.session.refresh(external_experiment_link)
        return external_experiment_link


@api.route('/external_experiment_links/<int:id>', endpoint='external_experiment_link')
class ExternalExperimentAPI(Resource):
    @http_auth_required
    @api.marshal_with(external_experiment)
    @api.response(200, 'Success')
    @api.response(404, 'Cannot find specified external experiment')
    def get(self, id: int):
        external_experiment_link = models.ExternalExperimentLinks.query.filter(models.ExternalExperimentLinks.id == id).one_or_none()
        if external_experiment_link is None:
            abort(404)
        return external_experiment_link
