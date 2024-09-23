import asyncio
import time

from PySide6.QtCore import Signal

from utils.common import commonProgram


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


# 引入配置文件
myConfig = commonProgram.EnableConfigHandler()
print(f'{__name__} get config Version', myConfig.version)
time_tracker = commonProgram.EnableTimeTracker()


@time_tracker.track_time
def sync_example():
    time.sleep(1)
    print("Synchronous Done")


@time_tracker.track_time
async def async_example():
    await asyncio.sleep(1)
    print("Asynchronous Done")


if __name__ == "__main__":
    # 多次调用同步函数
    for _ in range(3):
        sync_example()

    # 多次调用异步函数
    asyncio.run(async_example())

    # 输出所有函数的执行时间
    time_tracker.log_all_times()

    # 输出特定函数的执行时间
    time_tracker.log_single_time("sync_example")
    time_tracker.log_single_time("async_example")
