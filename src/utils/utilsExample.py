class UtilsExample:
    # 声明带一个字典类型参数的信号
    mainSignal = Signal(dict)  # 主界面的信号用来绑定子界面类的函数方法

    def __init__(self):
        # 引入公共程序
        from utils.common import commonProgram
        # 引入配置文件
        self.myConfig = commonProgram.EnableConfigHandler()
        print('MainWindow get config Version', self.myConfig.version)
        # 引入可控串口信息窗口
        self.serialPortWin = commonProgram.EnableSerialPort(winSignal=self.mainSignal,
                                                            RecvSerialData=self.RecvSerialData)

    def RecvSerialData(self, dictData: dict):
        # 用于接收Form2发过来的数据
        # dataStr = dictData.get("data", None)  # num2 就是子界面传递过来的数据
        # self.RecvDataHandle(dictData)
        pass
