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


from .base import api
from .summary_models import experiment_summary
from ... import models
from ...exceptions import CouldNotFindResourceError

db = models.db


scantype = api.model('ScanType', {
    'id': fields.Integer,
    'uri': fields.Url('api_v2.scantype'),
    'modality': fields.String,
    'protocol': fields.String,
})

scan_get = api.model('ScanGet', {
    'id': fields.Integer,
    'uri': fields.Url('api_v2.scan'),
    'experiment': fields.Nested(experiment_summary),
    'scantype': fields.Nested(scantype)
})

scan_list = api.model('ScanList', {
    'scans': fields.List(fields.Nested(scan_get))
})



@api.route('/scans', endpoint='scans')
class ScanListAPI(Resource):
    request_parser = reqparse.RequestParser()
    request_parser.add_argument('scantype_protocol', type=str, required=True, location='json',
                                help='No scantype protocol specified')
    request_parser.add_argument('experiment_id', type=int, required=True, location='json',
                                help='No experiment id specified')

    @http_auth_required
    @api.marshal_with(scan_list)
    @api.response(200, 'Success')
    def get(self):
        scans = models.Scan.query.order_by(models.Scan.id).all()
        return {'scans': scans}

    @http_auth_required
    @permissions_accepted('sample_add')
    @api.marshal_with(scan_get)
    @api.response(201, 'Created')
    def post(self):
        args = self.request_parser.parse_args()
        scantype_protocol, experiment_id = args.get("scantype_protocol"), args.get("experiment_id")
        # Find the experiment
        experiment = models.Experiment.query.filter(models.Experiment.id == experiment_id).one_or_none()
        if experiment is None:
            raise CouldNotFindResourceError(experiment_id, models.Experiment)

        # Find the scantype
        scantype = models.Scantype.query.filter(models.Scantype.protocol == scantype_protocol).one_or_none()
        if scantype is None:
            raise CouldNotFindResourceError(scantype, models.Scantype)

        scan = models.Scan(experiment=experiment, scantype=scantype)

        db.session.add(scan)
        db.session.commit()
        db.session.refresh(scan)

        return scan, 201


@api.route('/scans/<int:id>', endpoint='scan')
class ScanAPI(Resource):
    
    @http_auth_required
    @api.marshal_with(scan_get)
    @api.response(200, 'Success')
    @api.response(404, 'Requested scan not found')
    def get(self, id):
        scan = models.Scan.query.filter(models.Scan.id == id).one_or_none()
        if scan is None:
            abort(404)
        return scan


scan_type_list = api.model('ScanTypeList', {
    'scantypes': fields.List(fields.Nested(scantype))
})


@api.route('/scantypes', endpoint='scantypes')
class ScantypeListAPI(Resource):
    @http_auth_required
    @api.marshal_with(scan_type_list)
    @api.response(200, 'Success')
    def get(self):
        scantypes = models.Scantype.query.order_by(models.Scantype.id).all()
        return {'scantypes': scantypes}


@api.route('/scantypes/<int:id>', endpoint='scantype')
class ScantypeAPI(Resource):
    @http_auth_required
    @api.marshal_with(scantype)
    @api.response(200, 'Success')
    @api.response(404, 'Could not find specified scantype')
    def get(self, id):
        scantype = models.Scantype.query.filter(models.Scantype.id == id).one_or_none()
        if scantype is None:
            abort(404)
        return scantype

