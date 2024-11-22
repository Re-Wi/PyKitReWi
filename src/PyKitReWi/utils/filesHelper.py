def ProcessFileRemoveCertainRows(input_file, output_file, line_ranges_to_remove: list):
    """
    从输入文件中删除指定的行数范围，并将剩余的内容保存到输出文件中。

    :example
    `# 定义要删除的行数区间列表
    ranges_to_remove = [(2, 4), (7, 9)]
    # 调用函数
    ProcessFileRemoveCertainRows('input.txt', 'output.txt', ranges_to_remove)
    `
    :param input_file: 输入文件的路径
    :param output_file: 输出文件的路径
    :param line_ranges_to_remove: 要删除的行数范围列表，每个元素是一个包含开始和结束行号的元组
    """
    # 读取原始文件内容
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # 对行数区间进行排序
    line_ranges_to_remove.sort()

    # 根据line_ranges_to_remove中的行数区间删除相应行
    lines_to_keep = []
    for i, line in enumerate(lines, start=1):
        should_remove = False
        for start, end in line_ranges_to_remove:
            if start <= i <= end:
                should_remove = True
                break
        if not should_remove:
            lines_to_keep.append(line)

    # 将剩余内容保存到新文件
    with open(output_file, 'w', encoding='utf-8') as f:
        f.writelines(lines_to_keep)


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
