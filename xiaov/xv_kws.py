import logging
from xv_wav import xv_wav
import asyncio, base64

from snowboy import snowboydecoder

class xv_kws:

    def __init__(self, model = None):
        self.wav = xv_wav()
        """ self.audio_frames 语音帧
        大概1s/12帧，安每秒的list存入dict内 {"":["","","","","","","","","","","","",""],"":["","","","","","","","","","","","",""]......} """
        self.audio_frames = {}
        """ self.audio_seconds 需要识别语音片段，每秒一个dict元素 {"":"", "":""} """
        self.audio_seconds = {}
        if model is None:
            self.model = 'snowboy'
        if self.model == 'snowboy':
            # 识别模型 snowboy
            logging.info('loaded snowboy')
            sensitivity = 0.5
            model_file = '/home/app/xiaov/snowboy/xiaov.pmdl'
            self.kws = snowboydecoder.HotwordDetector(model_file, sensitivity=sensitivity)
    
    def detect(self, data):
        """ 识别 """
        if self.model == 'snowboy':
            return self.kws.detector.RunDetection(data)
        return False
    
    async def main(self, params):
        """ 语音唤醒主流程
        接收语音片段，大约1秒上传12次回调
        上传的语音，会有先后顺序乱、丢包丢帧等问题，需要前端生产顺序
        接收语音，进行拼接，拼接1s语音

        param params: 帧数据，{uuid:uuid, id:id, blob:base64} 
                      参数说明 uuid:当前1秒时间戳,id:当前帧顺序数字1-12,blob:wav二进制转base64数据
        """
        logging.debug('request')
        
        uuid = params['uuid']

        # 存储帧数据
        if self.audio_frames.get(uuid) is None:
            self.audio_frames[uuid] = {}
        self.audio_frames[uuid][params['id']] = base64.b64decode(params['blob'])

        # 当达到12帧，把12帧组合成为1s的语音片段数据，并清理self.audio_frames当前秒内12帧数据
        if len(self.audio_frames[uuid]) == 12:
            logging.debug('wav join')
            # 取出12帧的list
            audio_frame = self.audio_frames[uuid]
            # 清理本次12帧数据
            del self.audio_frames[uuid]
            # key排序，保证语音合成是按照时间顺序合成
            keys = sorted(audio_frame.keys(), reverse=False)
            # 安key取出相应语音片段
            frames = []
            for key in keys:
                frames.append(audio_frame[key])
            # 1s语音片段合并完成，赋值给self.audio_seconds
            data = self.wav.join(frames)
            # with open("./runtimes/tmp.wav", "wb") as f: # 本地写入测试
            #     f.write(data)
            self.audio_seconds[uuid] = data
        # KWS识别，利用snowboy
        if await self.recognition(self.audio_seconds):
            return True
        return False

    async def recognition(self, audio_seconds):
        # 提取s语音片段，并识别
        s = 1
        if len(audio_seconds) > s:
            logging.debug('recognition')
            # 删除第一秒
            del audio_seconds[list(audio_seconds.keys())[0]]
            # key排序，保证语音合成是按照时间顺序合成
            keys = sorted(audio_seconds.keys(), reverse=False)
            # 安key取出相应语音片段
            frams = []
            for key in keys:
                frams.append(audio_seconds[key])
            # 合并
            data = self.wav.join(frams)
            # with open("./runtimes/tmp.wav", "wb") as f:
            #     f.write(data)
            # 利用snowboy识别
            ans = self.detect(data)
            if ans == 1:
                logging.info('I am xiaov')
                return True
        return False
