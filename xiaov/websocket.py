import snowboydecoder
import websockets
import asyncio
import base64, json
import struct


## ------------------------------------ ##
# 接收语音片段，大约1秒上传12次回调
# 上传的语音，会有先后顺序乱、丢包丢帧等问题，需要前端生产顺序
# 接收语音，进行拼接，拼接1s语音
## ------------------------------------ ##

# 语音帧
# 大概1s/12帧，安每秒的list存入dict内
# {"":["","","","","","","","","","","","",""],"":["","","","","","","","","","","","",""]......}
audio_frames = {}

# 需要识别语音片段，每秒一个dict元素
# {"":"", "":""}
audio_seconds = {} 

# 初始化snowboy
sensitivity = 0.5
model_file = './xiaov.pmdl'
detection = snowboydecoder.HotwordDetector(model_file, sensitivity=sensitivity)

# websocket 服务
async def run(websocket, path):

    while True:
        # 接参，帧数据，json格式:{uuid:uuid, id:id, blob:base64}
        # 参数说明 uuid:当前1秒时间戳,id:当前帧顺序数字1-12,blob:wav二进制转base64数据
        request_data = await websocket.recv()
        params = json.loads(request_data)
        uuid = params['uuid']

        # 存储帧数据
        if audio_frames.get(uuid) is None:
            audio_frames[uuid] = {}
        audio_frames[uuid][params['id']] = base64.b64decode(params['blob'])

        # 当达到12帧，把12帧组合成为1s的语音片段数据，并清理audio_frames当前秒内12帧数据
        if len(audio_frames[uuid]) == 12:
            # 取出12帧的list
            audio_frame = audio_frames[uuid]
            # 清理本次12帧数据
            del audio_frames[uuid]
            # 1s语音片段合并完成，赋值给audio_seconds
            data = join_audio(audio_frame)
            # with open("./runtimes/tmp.wav", "wb") as f: # 本地写入测试
            #     f.write(data)
            audio_seconds[uuid] = data
        # KWS识别，利用snowboy
        if await recognition(audio_seconds):
            await websocket.send(f"ok")

        # await websocket.send(f"wait...")

        # await websocket.close() # 直接关闭连接

# 合并wav二进制
def join_audio(frams):
    # key排序，保证语音合成是按照时间顺序合成
    keys = sorted(frams.keys(), reverse=False)
    # 安key取出相应语音片段
    audio_frames = []
    for key in keys:
        audio_frames.append(frams[key])
    # 合并语音片段
    body = bytes()
    head = bytes()
    # 循环排序后的语音片段
    for item in audio_frames:
        if len(head) == 0:
            # 获取语音片段二进制的head头信息
            head = item[:44]
        # 拼接语音片段的二进制数据
        body = body + item[44:]
    # 更新WAV文件的总byte数，两个文件数据帧和+44
    head = head[:4] + struct.pack('<I', len(body)+44) + head[8:]
    head = head[:40] + struct.pack('<I', len(body)) + head[44:]
    # 拼接head头信息和body帧数据
    body = head + body
    return body

async def recognition(audio_seconds):
    # 提取s语音片段，并识别
    s = 1
    if len(audio_seconds) > s:
        # 删除第一秒
        del audio_seconds[list(audio_seconds.keys())[0]]
        # 合并
        data = join_audio(audio_seconds)
        # with open("./runtimes/tmp.wav", "wb") as f:
        #     f.write(data)
        # 利用snowboy识别
        ans = detection.detector.RunDetection(data)
        if ans == 1:
            return True
    return False

start_server = websockets.serve(run, "0.0.0.0", 8142)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
