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

import os
import json
import logging

__all__ = ['Config']


logger = logging.getLogger(__name__)


class _ConfigData(dict):
    """
    Dict with predefined keys.
    """
    _keys = ('url', 'a_token', 'r_token' 'device_id')

    def __init__(self, *args, **kwargs):
        for key in _ConfigData._keys:
            self.setdefault(key, '')

        super(_ConfigData, self).__init__(*args, **kwargs)


class Config(object):
    """
    Stores devicehive client configuration. Provides simple save/load interface.
    """
    _data_path = ''
    _data = None
    _update_callback = None

    def __init__(self, update_callback=None, config_filename='dh_config.json'):
        self._update_callback = update_callback
        self._data_path = os.path.join(os.getcwd(), config_filename)
        self._data = _ConfigData()

    def _on_update(self):
        self._update_callback()

    @property
    def data(self):
        return self._data

    def save(self, data):
        self._data.update(data)
        try:
            with open(self._data_path, "w") as f:
                json.dump(self._data, f, indent=4)
        except IOError:
            logger.info('Can\'t save "{}"'.format(self._data_path))
            return False

        logger.info('Successfully saved "{}"'.format(self._data_path))
        self._on_update()
        return True

    def load(self):
        try:
            with open(self._data_path, "r") as f:
                self._data = json.load(f, object_pairs_hook=_ConfigData)
        except IOError:
            logger.info('Can\'t load "{}"'.format(self._data_path))
            return False

        logger.info('Successfully loaded "{}"'.format(self._data_path))
        self._on_update()
        return True
