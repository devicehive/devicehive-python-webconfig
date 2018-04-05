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


class Status(object):
    """
    Represents devicehive connection status.
    """
    _status = None
    _last_error = ''

    def __init__(self):
        self._status = Status.DISCONNECTED

    CONNECTED = 'connected'
    CONNECTING = 'connecting'
    DISCONNECTED = 'disconnected'

    @property
    def status(self):
        return self._status

    @property
    def connected(self):
        return self.status == Status.CONNECTED

    @property
    def last_error(self):
        return self._last_error

    @property
    def data(self):
        return {
            'status': self.status,
            'error_message': self.last_error
        }

    def _set_status(self, status, error_message=''):
        self._status = status
        self._last_error = error_message

    def set_connected(self):
        self._set_status(Status.CONNECTED)

    def set_connecting(self):
        self._set_status(Status.CONNECTING)

    def set_disconnected(self, error=''):
        self._set_status(Status.DISCONNECTED, error)
