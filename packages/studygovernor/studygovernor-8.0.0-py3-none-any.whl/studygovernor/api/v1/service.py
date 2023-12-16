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

from flask_restx import fields, Resource
from flask_security import http_auth_required


from .base import api
from ...util.periodic_tasks import check_timeouts

check_timeouts_post = api.model('CheckTimeoutsPost', {
    'run_timeouts': fields.Integer,
    'wait_timeouts': fields.Integer,
})


@api.route('/service/check_timeouts', endpoint='check_timeouts')
class CheckTimeoutApi(Resource):
    @http_auth_required
    @api.marshal_with(check_timeouts_post)
    @api.response(200, 'Success')
    def post(self):
        run_timeouts, wait_timeouts = check_timeouts()

        return {
            'run_timeouts': run_timeouts,
            'wait_timeouts': wait_timeouts,
        }
