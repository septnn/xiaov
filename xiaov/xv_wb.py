import logging
import websockets
import asyncio


class xv_wb:

    model = None

    def __init__(self, main = None):
        """ Initialization a websocket
        """
        logging.info('Websocket init')
        self.main = main
        start_server = websockets.serve(main, "0.0.0.0", 8142)
        asyncio.get_event_loop().run_until_complete(start_server)
        asyncio.get_event_loop().run_forever()
