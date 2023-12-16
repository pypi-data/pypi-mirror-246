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
from ... import models, control

from ...fields import ObjectUrl, MappingField

db = models.db


cohort_list = api.model('CohortList', {
    'cohorts': fields.List(ObjectUrl('api_v1.cohort', attribute='id'))
})

cohort_get = api.model('CohortGet', {
    'uri': fields.Url('api_v1.cohort'),
    'label': fields.String,
    'description': fields.String,
    'external_urls': MappingField,
    'subjects': fields.List(ObjectUrl('api_v1.subject', attribute='id'))
})


cohort_post = api.model('CohortPost', {
    'label': fields.String,
    'description': fields.String,
})


@api.route('/cohorts', endpoint='cohorts')
class CohortListAPI(Resource):
    request_parser = reqparse.RequestParser()
    request_parser.add_argument('label', type=str, required=True, location='json',
                                help='No label specified')
    request_parser.add_argument('description', type=str, required=False, location='json',
                                help='Description of the cohort')

    @http_auth_required
    @api.marshal_with(cohort_list)
    @api.response(200, 'Success')
    def get(self):
        cohorts = models.Cohort.query.order_by(models.Cohort.id).all()

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


@api.route('/cohorts/<id>', endpoint='cohort')
class CohortAPI(Resource):
    request_parser_get = api.parser()
    request_parser_get.add_argument('filter_field', type=str, required=False, location='args', help='Should be either "id" or "label"')

    request_parser_post = reqparse.RequestParser()
    request_parser_post.add_argument('label', type=str, required=False, location='json')
    request_parser_post.add_argument('description', type=str, required=False, location='json')

    @http_auth_required
    @api.marshal_with(cohort_get)
    @api.response(200, 'Success')
    @api.response(404, 'Could not find specified cohort')
    @api.expect(request_parser_get)
    def get(self, id):
        args = self.request_parser_get.parse_args()

        if args['filter_field'] == 'id':
            try:
                id_ = int(id)
                cohort = models.Cohort.query.filter(models.Cohort.id == id_).one_or_none()
            except ValueError as excp:
                print(excp)
                cohort = None
        elif args['filter_field'] == 'label':
            label = str(id)
            cohort = models.Cohort.query.filter(models.Cohort.label == label).one_or_none()
        else:
            try:
                id_ = int(id)
                cohort = models.Cohort.query.filter(models.Cohort.id == id_).one()
            except (ValueError, NoResultFound):
                label = str(id)
                cohort = models.Cohort.query.filter(models.Cohort.label == label).one_or_none()

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
        args = self.request_parser_post.parse_args()
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


