import logging
from xv_wb import xv_wb
from xv_kws import xv_kws
import json, asyncio

# 默认日志
logging.getLogger().setLevel(logging.INFO)

class xv:

    def __init__(self):
        self.is_kws = False
        self.kws = xv_kws()
        self.websocket_server = xv_wb(main=self.main)
    
    async def main(self, websocket, path):
        """ websocket 入口函数
        """
        logging.info(__name__)
        while True:
            # 接参 json格式
            request = await websocket.recv()
            logging.debug(request)
            params = json.loads(request)

            if self.is_kws is False:
                response = await self.kws.main(params)
                if response is not False:
                    await websocket.send(f"ok")
                    self.is_kws = True
            else:
                # TODO something
                pass

        return True

if __name__ == "__main__":
    xiaov = xv()
