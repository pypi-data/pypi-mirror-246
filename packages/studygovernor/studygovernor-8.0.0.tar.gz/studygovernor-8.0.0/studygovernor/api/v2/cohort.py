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
from .summary_models import cohort_summary, subject_summary
from ... import models, control

from ...fields import MappingField

db = models.db


cohort_list = api.model('CohortList', {
    'cohorts': fields.List(
        fields.Nested(cohort_summary)
    )
})

cohort_get = api.model('CohortGet', {
    'id': fields.Integer,
    'label': fields.String,
    'uri': fields.Url('api_v2.cohort'),
    'description': fields.String,
    'external_urls': MappingField,
    'subjects': fields.List(fields.Nested(subject_summary))
})


cohort_post = api.model('CohortPost', {
    'label': fields.String,
    'description': fields.String,
})


@api.route('/cohorts', endpoint='cohorts')
class CohortListAPI(Resource):
    request_parser = reqparse.RequestParser()
    request_parser.add_argument('label', type=str, required=False, location='json',
                                help='No label specified')
    request_parser.add_argument('description', type=str, required=False, location='json',
                                help='Description of the cohort')

    @http_auth_required
    @api.marshal_with(cohort_list)
    @api.response(200, 'Success')
    def get(self):
        args = self.request_parser.parse_args()
        query = models.Cohort.query
        label = args.get('label')
        if label:
            query = query.filter(models.Cohort.label == label)
        cohorts = query.order_by(models.Cohort.id).all()

        return {
            'cohorts': cohorts,
        }

    @http_auth_required
    @permissions_accepted('sample_add')
    @api.marshal_with(cohort_get)
    @api.expect(cohort_post)
    @api.response(201, 'Created')
    def post(self):
        current_app.logger.info("[INFO] About to post cohort!")
        cohort = models.Cohort(**self.request_parser.parse_args())
        db.session.add(cohort)
        db.session.commit()
        db.session.refresh(cohort)

        return cohort, 201


@api.route('/cohorts/<int:id>', endpoint='cohort')
class CohortAPI(Resource):
    request_parser_put = reqparse.RequestParser()
    request_parser_put.add_argument('label', type=str, required=False, location='json')
    request_parser_put.add_argument('description', type=str, required=False, location='json')

    @http_auth_required
    @api.marshal_with(cohort_get)
    @api.response(200, 'Success')
    @api.response(404, 'Could not find specified cohort')
    def get(self, id):
        cohort = models.Cohort.query.filter(models.Cohort.id == id).one_or_none()
        if cohort is None:
            abort(404)
        return cohort

    @http_auth_required
    @permissions_accepted('sample_add')
    @api.marshal_with(cohort_get)
    @api.expect(cohort_post)
    @api.response(200, 'Success')
    @api.response(404, 'Could not find specified cohort')
    def put(self, id):
        args = self.request_parser_put.parse_args()
        cohort = models.Cohort.query.filter(models.Cohort.id == id).one_or_none()

        if cohort is None:
            abort(404)

        if args.get('label') is not None:
            cohort.label = args['label']
        if args.get('description') is not None:
            cohort.date_of_birth = args['description']

        db.session.commit()
        db.session.refresh(cohort)

        return cohort

@api.route('/cohorts/by-label/<label>', endpoint='cohort_by_label')
class CohortByLabelAPI(Resource):
    request_parser_put = reqparse.RequestParser()
    request_parser_put.add_argument('label', type=str, required=False, location='json')
    request_parser_put.add_argument('description', type=str, required=False, location='json')

    @http_auth_required
    @api.marshal_with(cohort_get)
    @api.response(200, 'Success')
    @api.response(404, 'Could not find specified cohort')
    def get(self, label):
        cohort = models.Cohort.query.filter(models.Cohort.label == label).one_or_none()
        if cohort is None:
            abort(404)
        return cohort


cohort_external_urls_get = api.model('CohortExternalUrlsGet', {
    'cohort_id': fields.Integer,
    'cohort_label': fields.String,
    'external_urls': MappingField
})

@api.route('/cohorts/<int:id>/external_urls', endpoint='cohort_external_urls')
class CohortExternalIdsAPI(Resource):
    post_request_parser = reqparse.RequestParser()
    post_request_parser.add_argument('external_urls', type=dict, required=True, location='json',
                                help='No external urls supplied')
    
    @http_auth_required
    @api.marshal_with(cohort_external_urls_get)
    @api.response(200, 'Success')
    @api.response(404, 'Could not find specified cohort')
    def get(self, id):
        cohort = models.Cohort.query.filter(models.Cohort.id == id).one_or_none()
        if cohort is None:
            abort(404)
        return {
            'cohort_id': cohort.id,
            'cohort_label': cohort.label,
            'external_urls': cohort.external_urls
        }

    @http_auth_required
    @permissions_accepted('sample_update')
    @api.expect(post_request_parser)
    @api.marshal_with(cohort_external_urls_get)
    @api.response(201, 'Added external urls')
    @api.response(404, 'Could not find specified cohort or external system')
    def post(self,id):
        args = self.post_request_parser.parse_args()
        external_urls = args['external_urls']

        cohort = models.Cohort.query.filter(models.Cohort.id == id).one_or_none()
        if cohort is None:
            abort(404)
        
        new_external_urls = []

        for system_name, external_url in external_urls.items():
            external_system = models.ExternalSystem.query.filter(models.ExternalSystem.system_name == system_name).one_or_none()
            if external_system is None:
                abort(404)
            external_cohort_url = models.ExternalCohortUrls.query.filter_by(cohort=cohort, external_system=external_system).one_or_none()
        
            # Create link if it doesn't exist
            if external_cohort_url is None:
                external_cohort_url = models.ExternalCohortUrls(url=external_url, cohort=cohort, external_system=external_system)
                db.session.add(external_cohort_url)
            else:
                external_cohort_url.url = external_url
            
            new_external_urls.append(external_cohort_url)

        cohort.external_system_urls = new_external_urls

        db.session.commit()
        
        return {
            'cohort_id': cohort.id,
            'cohort_label': cohort.label,
            'external_urls': cohort.external_urls
        }, 201


@api.route('/cohorts/<int:id>/external_urls/<system_name>', endpoint='cohort_system_external_url')
class CohortExternalSystemUrlAPI(Resource):
    post_request_parser = reqparse.RequestParser()
    post_request_parser.add_argument('external_url', type=str, required=True, location='json',
                                help='No external urls supplied')
    
    
    @http_auth_required
    @permissions_accepted('sample_update')
    @api.expect(post_request_parser)
    @api.marshal_with(cohort_external_urls_get)
    @api.response(201, 'Changed external url')
    @api.response(404, 'Could not find specified cohort or external system')
    def put(self, id, system_name):
        args = self.post_request_parser.parse_args()
        external_url = args['external_url']

        cohort = models.Cohort.query.filter(models.Cohort.id == id).one_or_none()
        external_system = models.ExternalSystem.query.filter(models.ExternalSystem.system_name == system_name).one_or_none()
        
        if cohort is None or external_system is None:
            abort(404)
        
        external_cohort_url = models.ExternalCohortUrls.query.filter_by(cohort=cohort, external_system=external_system).one_or_none()
    
        # Create link if it doesn't exist
        if external_cohort_url is None:
            external_cohort_url = models.ExternalCohortUrls(url=external_url, cohort=cohort, external_system=external_system)
            db.session.add(external_cohort_url)
        else:
            external_cohort_url.url = external_url

        db.session.commit()
        
        return {
            'cohort_id': cohort.id,
            'cohort_label': cohort.label,
            'external_urls': cohort.external_urls
        }, 201

    @http_auth_required
    @permissions_accepted('sample_delete')
    @api.marshal_with(cohort_external_urls_get)
    @api.response(200, 'Success')
    @api.response(404, 'Could not find specified cohort, external system or external id')
    def delete(self, id, system_name):
        
        cohort = models.Cohort.query.filter(models.Cohort.id == id).one_or_none()
        external_system = models.Subject.query.filter(models.ExternalSystem.system_name == system_name).one_or_none()
        
        if cohort is None or external_system is None:
            abort(404)
        
        external_cohort_url = models.ExternalCohortUrls.query.filter_by(cohort=cohort, external_system=external_system).one_or_none()
    
        # Delete link if it exists
        if external_cohort_url is None:
            abort(404)
        else:
            db.session.delete(external_cohort_url)

        db.session.commit()
        
        return {
            'cohort_id': cohort.id,
            'cohort_label': cohort.label,
            'external_urls': cohort.external_urls
        }
