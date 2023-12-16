import datetime
import yaml

from flask import abort
from flask_restx import fields, Resource, reqparse
from flask_security import http_auth_required, roles_accepted


from .base import api
from .summary_models import role_summary
from .user import user_summary
from .scan import scantype
from .external_objects import external_system_model

from ... import models
from ...util.import_config import load_config

db = models.db


config_load_summary = api.model('ConfigSummary', {
    'updated_at': fields.DateTime(dt_format='iso8601'),
    'users': fields.List(fields.Nested(user_summary)),
    'roles': fields.List(fields.Nested(role_summary)),
    'external_systems': fields.List(fields.Nested(external_system_model)),
    'scantypes': fields.List(fields.Nested(scantype))
})

@api.route('/service/config/import-config', endpoint='config')
class ConfigAPI(Resource):
    
    request_parser = reqparse.RequestParser()
    request_parser.add_argument('config_definition',
                                        type=str,
                                        required=True,
                                        location='json',
                                        help='No label specified')
    
    @http_auth_required
    @roles_accepted('admin')
    @api.expect(request_parser)
    @api.marshal_with(config_load_summary)
    @api.response(201, 'Created')
    def post(self):
        args = self.request_parser.parse_args()
        config_definition = args.get('config_definition')
        
        try:
            config_definition = yaml.safe_load(config_definition)
        except yaml.YAMLError as exc:
            abort(400, f'Config definition is not a valid YAML file. {exc}')
        
        try:
            updated_objects = load_config(config_definition)
            db.session.commit()

            result = {
                'updated_at': datetime.datetime.now(),
                **updated_objects
            }
            
            return result, 201
        except:
            abort(400, 'Config definition is invalid.')
    

    @http_auth_required
    @roles_accepted('admin')
    @api.expect(request_parser)
    @api.marshal_with(config_load_summary)
    @api.response(200, 'Updated')
    def put(self):
        args = self.request_parser.parse_args()
        config_definition = args.get('config_definition')
        
        try:
            config_definition = yaml.safe_load(config_definition)
        except yaml.YAMLError as exc:
            abort(400, f'Config definition is not a valid YAML file. {exc}')
        
        try:
            updated_objects = load_config(config_definition, overwrite=True)
            db.session.commit()

            result = {
                'updated_at': datetime.datetime.now(),
                **updated_objects
            }
            
            return result, 200
        except:
            abort(400, 'Config definition is invalid.')
