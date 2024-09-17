import binascii
import linecache
import os
import struct
import time


class BinHandler:
    fileName = ''
    binfile = None
    curLine = 0
    curLength = 0
    fileLines = 0

    def __init__(self, fileName):
        self.fileName = fileName
        self.binfile = open(self.fileName, 'rb')  # 打开二进制文件
        # self.fileSize = os.path.getsize(self.fileName)  # 获得文件大小
        self.fileLines = len(self.binfile.readlines())
        self.binfile.seek(0)

    def __del__(self):
        self.binfile.close()  # 关闭bin文件

    def GetFrame(self):
        # 超出行数，不会报错，返回空值
        # lineContent = linecache.getline(self.fileName, count)
        # 👆 不适用
        head = self.GetHead()
        self.curLength = self.GetLength()
        data = self.GetData(self.curLength[0] * 2 + 2)
        # print(head)
        # print(length)
        # print(data)
        dataBlock = head[0] + head[1] + self.curLength[1] + data
        # print(dataBlock)
        # print(dataBlock.encode('UTF-8'))
        # bytes().fromhex()
        self.curLine += 1
        # 去掉'\r\n'
        # self.binfile.read(2)
        return dataBlock.encode('UTF-8'), self.curLine

    def GetHead(self):
        data1 = self.binfile.read(1)  # 一次读取1个字节
        data2 = self.binfile.read(1)  # 一次读取1个字节
        data2 = int(data2)
        return data1.hex(), str(data2).zfill(2)

    def GetLength(self):
        data = self.binfile.read(2)  # 一次读取2个字节
        dataInt = int(data, 16)
        return dataInt, data.decode('UTF-8')

    def GetData(self, pCount):
        data = self.binfile.read(pCount)  # 一次读取pCount个字节
        return data.decode('UTF-8')

    def GetLine(self):
        with open(self.fileName, 'r') as file:
            line = file.readline()
            counts = 1
            while line:
                if counts >= 50000000:
                    break
                line = file.readline()
                counts += 1


# 程序入口
if __name__ == '__main__':
    binHandler = BinHandler('C:/Users/18710/Desktop/ExteriorMirror/PythonComTool/BL_program.run')
    content = binHandler.GetFrame()
    print(content)
    content = binHandler.GetFrame()
    print(content)
    content = binHandler.GetFrame()
    print(content)
    print(bytes().fromhex(content[0].decode('UTF-8')))
