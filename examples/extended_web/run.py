import os
from devicehive_webconfig import Server, Handler

from controllers import ExampleController

routes = [
    (r'^/example/$', ExampleController),
]


class ExampleHandler(Handler):
    pass


if __name__ == '__main__':
    s = Server(ExampleHandler, routes=routes,
               static_dirs=(os.path.join(os.path.dirname(__file__), 'static'),))
    s.start()
