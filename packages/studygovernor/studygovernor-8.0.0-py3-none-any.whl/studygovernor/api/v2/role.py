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
from flask_restx import fields, Resource
from flask_security import http_auth_required, permissions_accepted


from .base import api
from .summary_models import role_summary
from ... import models


db = models.db


role_get = api.model("RoleGet", {
    'id': fields.Integer,
    'name': fields.String,
    'uri': fields.Url('api_v2.role'),
    'description': fields.String,
    'update_datetime': fields.DateTime,
    'permissions': fields.List(fields.String)
})


role_list_get = api.model("RoleListGet", {
    'roles': fields.List(fields.Nested(role_summary))
})


@api.route('/roles', endpoint='roles')
class RoleListAPI(Resource):
    @http_auth_required
    @permissions_accepted('roles_manage')
    @api.marshal_with(role_list_get)
    @api.response(200, "Success")
    def get(self):
        roles = models.Role.query.order_by(models.Role.id).all()
        return {"roles": roles}


@api.route('/roles/<int:id>', endpoint='role')
class RoleApi(Resource):
    @http_auth_required
    @permissions_accepted('roles_manage')
    @api.marshal_with(role_get)
    @api.response(200, "Success")
    @api.response(404, "Could not find role")
    def get(self, id):
        role = models.Role.query.filter_by(id=id).one_or_none()
        if role is None:
            abort(404)
        return {'name': role.name,
                'description': role.description,
                'update_datetime': role.update_datetime,
                'permissions': role.get_permissions()}

