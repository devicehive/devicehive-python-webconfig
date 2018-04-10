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

import time
import logging
import threading
from devicehive import DeviceHive, TransportError

from .web_server import WebServer
from .config import Config
from .status import Status
from .base.handler import RoutedHandler


logger = logging.getLogger(__name__)


__all__ = ['Server']


class Server(object):
    """
    Encapsulates DeviceHive connection and web server. Can be easily extended to
    add more services to run.
    """
    dh_cfg = None
    dh_status = None
    deviceHive = None
    webServer = None

    _dh_thread = None
    _web_thread = None
    _dh_handler_class = None
    _dh_handler_args = None
    _dh_handler_kwargs = None

    _is_blocking = None
    __is_running = None

    def __init__(self, dh_handler_class, routes=(), static_dirs=(),
                 is_blocking=True, server_address=('0.0.0.0', 8000),
                 initial_config=None, *dh_handler_args, **dh_handler_kwargs):
        """
        Initialize web server and devicehive client.
        :param dh_handler_class: Handler class for devicehive client.
        :param routes: Additional routes for web server.
        :param static_dirs: Additional static dirs for web server.
        :param is_blocking: If True blocking loop wil be started on startup.
        :param server_address: Server address to serve web ui.
        :param initial_config: Dict with Devicehive config.
        :param dh_handler_args: Additional args to be passed to handler.
        :param dh_handler_kwargs: Additional kwargs to be passed to handler.
        """
        self._dh_handler_class = dh_handler_class
        self._dh_handler_args = dh_handler_args
        self._dh_handler_kwargs = dh_handler_kwargs
        self._is_blocking = is_blocking
        self._initial_config = initial_config

        self.dh_status = Status()
        self.dh_cfg = Config(update_callback=self._restart_dh)
        self.webServer = WebServer(server=self, routes=routes,
                                   static_dirs=static_dirs,
                                   server_address=server_address,
                                   RequestHandlerClass=RoutedHandler)

        self._web_thread = threading.Thread(
            target=self._web_loop, name='web')
        self._web_thread.setDaemon(True)

    @property
    def is_running(self):
        return self.__is_running

    def start(self):
        self.__is_running = True
        self._start_web()

        # this will start DH thread automatically
        if self._initial_config:
            self.dh_cfg.save(self._initial_config)
        else:
            self.dh_cfg.load()

        self._on_startup()

        if self._is_blocking:
            self._blocking_loop()

    def stop(self):
        self.__is_running = False
        self.webServer.shutdown()
        self._stop_dh()

        self._on_shutdown()

    def _on_startup(self):
        """
        Can be overridden by nested classes to start additional processes
        """
        pass

    def _on_shutdown(self):
        """
        Can be overridden by nested classes to stop additional processes
        """
        pass

    def _blocking_loop(self):
        try:
            while self.__is_running:
                time.sleep(.001)
        except KeyboardInterrupt:
            logger.info(
                'Warm shutdown request by Ctrl-C. Press again to use force.')
            try:
                self.stop()
            except KeyboardInterrupt:
                logger.info('May the force be with you!')
                raise

    def _web_loop(self):
        self.webServer.serve_forever()

    def _dh_loop(self):
        self.deviceHive = DeviceHive(self._dh_handler_class,
                                     device_id=self.dh_cfg.data['device_id'],
                                     connect_cb=self._dh_connect,
                                     *self._dh_handler_args,
                                     **self._dh_handler_kwargs)
        error = ''
        try:
            self.dh_status.set_connecting()
            url = self.dh_cfg.data['url']
            access_token = self.dh_cfg.data['a_token']
            refresh_token = self.dh_cfg.data['r_token']
            self.deviceHive.connect(url, access_token=access_token,
                                    refresh_token=refresh_token)
        except TransportError as e:
            logger.exception(e)
            error = str(e)
        finally:
            self.dh_status.set_disconnected(error)
            logger.info('Stop devicehive')

    def _dh_connect(self):
        self.dh_status.set_connected()

    def _start_web(self):
        logger.info('Start web server on http://{}:{}'.format(
            *self.webServer.server_address))
        self._web_thread.start()

    def _start_dh(self):
        if self.dh_status.connected:
            logging.info('Devicehive already started')
            return

        logger.info('Start devicehive')
        self._dh_thread = threading.Thread(
            target=self._dh_loop, name='device_hive')
        self._dh_thread.setDaemon(True)
        self._dh_thread.start()

    def _stop_dh(self):
        if not self.dh_status.connected:
            logging.info('Devicehive already stopped')
            return
        self.deviceHive.handler.api.disconnect()

        logging.info('Stoping devicehive...')
        self._dh_thread.join()

    def _restart_dh(self):
        if self.dh_status.connected:
            self._stop_dh()

        self._start_dh()
