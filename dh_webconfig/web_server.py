import os
from six.moves.BaseHTTPServer import HTTPServer
from six.moves.socketserver import ThreadingMixIn

from .routes import routes as default_routes


class WebServer(ThreadingMixIn, HTTPServer):
    """
    Web server that provides simple route system.
    """
    daemon_threads = True
    _server = None
    _routes = default_routes
    _static_dirs = [os.path.join(os.path.dirname(__file__), 'static')]

    def __init__(self, server, routes=(), static_dirs=(), *args, **kwargs):
        self._server = server
        self._routes.extend(routes)
        self._static_dirs.extend(static_dirs)
        HTTPServer.__init__(self, *args, **kwargs)

    @property
    def routes(self):
        return self._routes

    @property
    def static_dirs(self):
        return self._static_dirs

    @property
    def server(self):
        return self._server

    @property
    def dh_cfg(self):
        return self._server.dh_cfg

    @property
    def dh_status(self):
        return self._server.dh_status
