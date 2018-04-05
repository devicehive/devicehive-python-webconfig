from six.moves import http_client
from devicehive_webconfig.base import Controller


class ExampleController(Controller):
    def get(self, handler, *args, **kwargs):
        response = self.render_template('example.html')

        handler.send_response(http_client.OK)
        handler.send_header('Content-type', 'text/html')
        handler.end_headers()
        handler.wfile.write(response.encode())
