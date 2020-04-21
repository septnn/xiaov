import logging
from xv_wb import xv_wb
from xv_kws import xv_kws

import json
import asyncio


# 默认日志
logging.getLogger().setLevel(logging.INFO)

class xv:

    kws = None
    websocket_server = None

    is_kws = False

    def __init__(self):
        self.kws = xv_kws()
        logging.info('loaded kws')

        logging.info('loaded websocket')
        self.websocket_server = xv_wb(main=self.main)
    
    async def main(self, websocket, path):
        """ websocket 入口函数
        """
        logging.info(__name__)
        while True:
            # 接参，帧数据，json格式:{uuid:uuid, id:id, blob:base64}
            # 参数说明 uuid:当前1秒时间戳,id:当前帧顺序数字1-12,blob:wav二进制转base64数据
            request = await websocket.recv()
            logging.debug(request)
            params = json.loads(request)

            if self.is_kws is False:
                response = await self.kws.request(params)
                if response is not False:
                    await websocket.send(f"ok")
                    self.is_kws = True
            else:
                # TODO something
                

        return True


if __name__ == "__main__":
    xiaov = xv()