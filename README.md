[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)

# Devicehive python web configurator
This is proxy package for [devicehive-python](https://github.com/devicehive/devicehive-python) that provides simple web interface to configure connection.

## Installation
```bash
pip install devicehive-webconfig
```

## Usage
### Basics
Web interface based on python HttpServer and implements Devicehive connection in separated thread.\
It takes _Handler_ class as argument like original _Devicehive_ class.\
Only difference that extended _Handler_ class from this repository must used.\
Server could be runned in non-blocking mode, so main thread is free to use.\
Example:

```python
import time
import json

from devicehive_webconfig import Server, Handler


class ExampleHandler(Handler):
    _device = None

    def handle_connect(self):
        self._device = self.api.put_device(self._device_id)
        super(ExampleHandler, self).handle_connect()

    def send(self, data):
        self._device.send_notification(data)


if __name__ == '__main__':
    server = Server(ExampleHandler, is_blocking=False)
    server.start()

    print('Go to http://127.0.0.1:8000/ and configure your connection.')
    while not server.dh_status.connected:
        # Wait till DH connection is ready
        time.sleep(.001)

    for i in range(10):
        server.deviceHive.handler.send('notification #{}'.format(i))

```
Additional _Handler_ arguments can be passed as _args_ and _kwargs_

### Advanced
This library was designed to be easily extended.
Additional routes, controllers, templates and static files can be added.
There is an [example](examples/extended_web) that shows how this can be done.
