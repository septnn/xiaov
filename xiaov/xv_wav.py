import struct

class xv_wav:

    def join(self, frams = []):
        """ 合并wav二进制

        param frams: 有序的语音帧二进制
        """
        # 合并语音片段
        body = bytes()
        head = bytes()
        # 循环排序后的语音片段
        for item in frams:
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




# wav head格式化
# 参见 (https://docs.python.org/zh-cn/3/library/struct.html?highlight=struct#)
# print(struct.unpack('<4s', bytes(blob[:4]))) # ‘RIFF‘文件标志
# print(struct.unpack('<I', bytes(blob[4:8]))) # 文件总长
# print(struct.unpack('<4s', bytes(blob[8:12]))) # ‘WAVE‘文件标志
# print(struct.unpack('<4s', bytes(blob[12:16]))) # ‘fmt‘标志
# print(struct.unpack('<I', bytes(blob[16:20]))) # 块长度
# print(struct.unpack('<H', bytes(blob[20:22]))) # PCM格式类别
# print(struct.unpack('<H', bytes(blob[22:24]))) # 声道数目
# print(struct.unpack('<I', bytes(blob[24:28]))) # 采样率
# print(struct.unpack('<I', bytes(blob[28:32]))) # 传输速率
# print(struct.unpack('<H', bytes(blob[32:34]))) # 数据块对齐单位 采样帧大小
# print(struct.unpack('<H', bytes(blob[34:36]))) # 每样本bit数 采样位数
# print(struct.unpack('<4s', bytes(blob[36:40]))) # data 标志
# print(struct.unpack('<I', bytes(blob[40:44]))) # 数据大小