from devicehive import Handler as DHHandler

__all__ = ['Handler']


class Handler(DHHandler):
    """
    Proxy handler for devicehive
    """
    _device_id = None
    _connect_cb = None

    def __init__(self, api, device_id, connect_cb):
        self._device_id = device_id
        self._connect_cb = connect_cb
        super(Handler, self).__init__(api)

    def handle_connect(self):
        self._connect_cb()
