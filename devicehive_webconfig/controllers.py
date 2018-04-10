# Copyright (C) 2018 DataArt
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

import json
from six.moves import http_client

from .base import BaseController, Controller

__all__ = ['Config', 'DHStatusUpdate']


class Config(Controller):

    def get(self, handler, *args, **kwargs):
        cfg_data = handler.server.dh_cfg.data
        status = handler.server.dh_status.status
        response = self.render_template('index.html', status=status, **cfg_data)

        handler.send_response(http_client.OK)
        handler.send_header('Content-type', 'text/html')
        handler.end_headers()
        handler.wfile.write(response.encode())

    def post(self, handler, *args, **kwargs):
        data = handler.post_vars
        new_data = {
            'url': data.get("url")[0],
            'a_token': data.get("a_token")[0],
            'r_token': data.get("r_token")[0],
            'device_id': data.get("device_id")[0],
        }
        handler.server.dh_cfg.save(new_data)

        handler.send_response(http_client.FOUND)
        handler.send_header('Location', '/')
        handler.end_headers()


class DHStatusUpdate(BaseController):

    def get(self, handler, *args, **kwargs):
        response = json.dumps({
            'status': handler.server.dh_status.status,
            'error_message': handler.server.dh_status.last_error
        })

        handler.send_response(http_client.OK)
        handler.send_header('Content-type', 'application/json')
        handler.end_headers()
        handler.wfile.write(response.encode())
