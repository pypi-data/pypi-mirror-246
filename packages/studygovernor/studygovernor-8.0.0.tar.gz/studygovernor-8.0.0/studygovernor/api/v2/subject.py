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

from flask import abort, current_app
from flask_restx import fields, Resource, reqparse, inputs
from flask_security import http_auth_required, permissions_accepted
from sqlalchemy.orm.exc import NoResultFound


from .base import api
from .summary_models import cohort_summary, experiment_summary, subject_summary
from .experiment import experiment_list, experiment_get
from ... import models, control
from ...exceptions import CouldNotFindResourceError 

from ...fields import MappingField

db = models.db


subject_list = api.model('SubjectList', {
    'subjects': fields.List(fields.Nested(subject_summary))
})

subject_get = api.model('SubjectGet', {
    'id': fields.Integer,
    'label': fields.String,
    'uri': fields.Url('api_v2.subject'),
    'api_uri': fields.String,
    'web_uri': fields.String,
    'cohort': fields.Nested(cohort_summary, allow_null=True),
    'date_of_birth': fields.String,
    'external_ids': MappingField,
    'experiments': fields.List(fields.Nested(experiment_summary))
})


@api.route('/subjects', endpoint='subjects')
class SubjectListAPI(Resource):
    get_request_parser = reqparse.RequestParser()
    get_request_parser.add_argument('cohort_label', type=str, required=False, location='args', help="Cohort label")
    get_request_parser.add_argument('offset', type=int, required=False, location='args', help="Offset for pagination")
    get_request_parser.add_argument('limit', type=int, required=False, location='args', help="Maximum number of rows returned")

    post_request_parser = reqparse.RequestParser()
    post_request_parser.add_argument('label', type=str, required=True, location='json',
                                help='No label specified')
    post_request_parser.add_argument('cohort_label', type=str, required=True, location='json', help="Cohort label")
    post_request_parser.add_argument('date_of_birth', type=inputs.date, required=True, location='json',
                                help='No date_of_birth specified')

    @http_auth_required
    @api.marshal_with(subject_list)
    @api.expect(get_request_parser)
    @api.response(200, 'Success')
    def get(self):
        args = self.get_request_parser.parse_args()
        offset = args['offset']
        limit = args['limit']
        cohort_label = args['cohort_label']

        subjects, count = control.get_subjects(cohort_label=cohort_label, offset=offset, limit=limit)
        return {
            'subjects': subjects,
            'offset': offset,
            'limit': limit,
            'count': count,
        }

    @http_auth_required
    @permissions_accepted('sample_add')
    @api.marshal_with(subject_get)
    @api.expect(post_request_parser)
    @api.response(201, 'Created')
    def post(self):
        current_app.logger.info("[INFO] About to post subject!")
        args = self.post_request_parser.parse_args()
        cohort_label = args.get("cohort_label")

        cohort = models.Cohort.query.filter(models.Cohort.label == args['cohort_label']).one_or_none()
        if cohort is None:
            raise CouldNotFindResourceError(cohort_label, models.Cohort)
        
        subject = models.Subject(label=args['label'], date_of_birth=args['date_of_birth'], cohort=cohort)
        
        db.session.add(subject)
        db.session.commit()
        db.session.refresh(subject)

        return subject, 201


@api.route('/subjects/<int:id>', endpoint='subject')
class SubjectAPI(Resource):
    
    put_request_parser = reqparse.RequestParser()
    put_request_parser.add_argument('label', type=str, required=False, location='json')
    put_request_parser.add_argument('cohort_label', type=str, required=False, location='json')
    put_request_parser.add_argument('date_of_birth', type=inputs.date, required=False, location='json')

    @http_auth_required
    @api.marshal_with(subject_get)
    @api.response(200, 'Success')
    @api.response(404, 'Could not find specified subject')
    def get(self, id):
        subject = models.Subject.query.filter(models.Subject.id == id).one_or_none()

        if subject is None:
            abort(404)

        return subject

    @http_auth_required
    @permissions_accepted('sample_add')
    @api.marshal_with(subject_get)
    @api.expect(put_request_parser)
    @api.response(200, 'Success')
    @api.response(404, 'Could not find specified subject')
    def put(self, id):
        args = self.put_request_parser.parse_args()
        subject = models.Subject.query.filter(models.Subject.id == id).one_or_none()

        if subject is None:
            abort(404)

        if args.get('label') is not None:
            subject.label = args['label']
        if args.get('date_of_birth') is not None:
            subject.date_of_birth = args['date_of_birth']
        if args.get('cohort_label') is not None:
            cohort = models.Cohort.query.filter(models.Cohort.label == args['cohort_label']).one_or_none()
            if cohort is None:
                abort(404)
            subject.cohort = cohort

        db.session.commit()
        db.session.refresh(subject)

        return subject


external_ids_get = api.model('SubjectExternalIdsGet', {
    'subject_id': fields.Integer,
    'subject_label': fields.String,
    'external_ids': MappingField
})

@api.route('/subjects/<int:id>/external_ids', endpoint='subject_external_ids')
class SubjectExternalIdsAPI(Resource):
    post_request_parser = reqparse.RequestParser()
    post_request_parser.add_argument('external_ids', type=dict, required=True, location='json',
                                help='No external ids supplied')
    
    @http_auth_required
    @api.marshal_with(external_ids_get)
    @api.response(200, 'Success')
    @api.response(404, 'Could not find specified subject')
    def get(self, id):
        subject = models.Subject.query.filter(models.Subject.id == id).one_or_none()
        if subject is None:
            abort(404)
        return {
            'subject_id': subject.id,
            'subject_label': subject.label,
            'external_ids': subject.external_ids
        }

    @http_auth_required
    @permissions_accepted('sample_update')
    @api.expect(post_request_parser)
    @api.marshal_with(external_ids_get)
    @api.response(201, 'Added external ids')
    @api.response(404, 'Could not find specified subject or external system')
    def post(self,id):
        args = self.post_request_parser.parse_args()
        external_ids = args['external_ids']

        subject = models.Subject.query.filter(models.Subject.id == id).one_or_none()
        if subject is None:
            abort(404)

        new_external_links = []
        
        for system_name, external_id in external_ids.items():
            external_system = models.ExternalSystem.query.filter(models.ExternalSystem.system_name == system_name).one_or_none()
            if external_system is None:
                abort(404)
            external_subject_link = models.ExternalSubjectLinks.query.filter_by(subject=subject, external_system=external_system).one_or_none()
        
            # Create link if it doesn't exist
            if external_subject_link is None:
                external_subject_link = models.ExternalSubjectLinks(external_id=external_id, subject=subject, external_system=external_system)
                db.session.add(external_subject_link)
            else:
                external_subject_link.external_id = external_id
            new_external_links.append(external_subject_link)
        
        subject.external_subject_links = new_external_links

        db.session.commit()
        
        return {
            'subject_id': subject.id,
            'subject_label': subject.label,
            'external_ids': subject.external_ids
        }, 201


@api.route('/subjects/<int:id>/external_ids/<system_name>', endpoint='subject_system_external_id')
class SubjectExternalSystemIdAPI(Resource):
    put_request_parser = reqparse.RequestParser()
    put_request_parser.add_argument('external_id', type=str, required=True, location='json',
                                help='No external ids supplied')
    
    @http_auth_required
    @permissions_accepted('sample_update')
    @api.expect(put_request_parser)
    @api.marshal_with(external_ids_get)
    @api.response(201, 'Changed external id')
    @api.response(404, 'Could not find specified subject or external system')
    def put(self, id, system_name):
        args = self.put_request_parser.parse_args()
        external_id = args['external_id']

        subject = models.Subject.query.filter(models.Subject.id == id).one_or_none()
        external_system = models.ExternalSystem.query.filter(models.ExternalSystem.system_name == system_name).one_or_none()
        
        if subject is None or external_system is None:
            abort(404)
        
        external_subject_link = models.ExternalSubjectLinks.query.filter_by(subject=subject, external_system=external_system).one_or_none()
    
        # Create link if it doesn't exist
        if external_subject_link is None:
            external_subject_link = models.ExternalSubjectLinks(external_id=external_id, subject=subject, external_system=external_system)
            db.session.add(external_subject_link)
        else:
            external_subject_link.external_id = external_id

        db.session.commit()
        
        return {
            'subject_id': subject.id,
            'subject_label': subject.label,
            'external_ids': subject.external_ids
        }, 201

    @http_auth_required
    @permissions_accepted('sample_delete')
    @api.marshal_with(external_ids_get)
    @api.response(200, 'Success')
    @api.response(404, 'Could not find specified subject, external system or external id')
    def delete(self, id, system_name):
        
        subject = models.Subject.query.filter(models.Subject.id == id).one_or_none()
        external_system = models.Subject.query.filter(models.ExternalSystem.system_name == system_name).one_or_none()
        
        if subject is None or external_system is None:
            abort(404)
        
        external_subject_link = models.ExternalSubjectLinks.query.filter_by(subject=subject, external_system=external_system).one_or_none()
    
        # Delete link if it exists
        if external_subject_link is None:
            abort(404)
        else:
            db.session.delete(external_subject_link)

        db.session.commit()
        
        return {
            'subject_id': subject.id,
            'subject_label': subject.label,
            'external_ids': subject.external_ids
        }

@api.route('/cohorts/<label>/subjects', endpoint='cohort_subjects')
class CohortSubjectsAPI(Resource):
    
    @http_auth_required
    @api.marshal_with(subject_list)
    @api.response(200, 'Success')
    @api.response(404, 'Could not find specified cohort')
    def get(self, label):
        cohort = models.Cohort.query.filter(models.Cohort.label == label).one_or_none()
        if cohort is None:
            abort(404)
        return {'subjects': cohort.subjects}

@api.route('/cohorts/<label>/subjects/<subject_label>', endpoint='cohort_subjects_label')
class CohortSubjectByLabelAPI(Resource):
    
    @http_auth_required
    @api.marshal_with(subject_get)
    @api.response(200, 'Success')
    @api.response(404, 'Could not find specified cohort or subject')
    def get(self, label, subject_label):
        subject = models.Subject.query.filter((models.Subject.cohort.has(label=label)) & (models.Subject.label == subject_label)).one_or_none()
        if subject is None:
            abort(404)
        return subject

@api.route('/cohorts/<label>/subjects/<subject_label>/experiments', endpoint='cohort_subjects_label_experiments')
class CohortSubjectExperimentsAPI(Resource):
    
    @http_auth_required
    @api.marshal_with(experiment_list)
    @api.response(200, 'Success')
    @api.response(404, 'Could not find specified cohort or subject')
    def get(self, label, subject_label):
        subject = models.Subject.query.filter((models.Subject.cohort.has(label=label)) & (models.Subject.label == subject_label)).one_or_none()
        if subject is None:
            abort(404)
        return {"experiments": subject.experiments}

@api.route('/cohorts/<label>/subjects/<subject_label>/experiments/<experiment_label>', endpoint='cohort_subjects_label_experiment')
class CohortSubjectExperimentAPI(Resource):
    
    @http_auth_required
    @api.marshal_with(experiment_get)
    @api.response(200, 'Success')
    @api.response(404, 'Could not find specified cohort, subject, or experiment')
    def get(self, label, subject_label, experiment_label):
        experiment = db.session.query(models.Experiment).join(models.Subject).join(models.Cohort).filter(
            (models.Cohort.label==label)&
            (models.Subject.label==subject_label)&
            (models.Experiment.label == experiment_label)).one_or_none()

        if experiment is None:
            abort(404)

        return experiment