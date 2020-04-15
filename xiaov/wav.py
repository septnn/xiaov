

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