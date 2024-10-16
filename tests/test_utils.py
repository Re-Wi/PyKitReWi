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
def sync_example(x):
    time.sleep(x)
    print("Synchronous Done --> ", x)
    return x * 2


@time_tracker.track_time
async def async_example(x):
    await asyncio.sleep(x)
    print("Asynchronous Done --> ", x)
    return x * 3


if __name__ == "__main__":
    # 多次调用同步函数
    for i in range(6):
        sync_example(i)


    # 多次调用异步函数
    async def main():
        # Call async_example multiple times
        await asyncio.gather(
            async_example(1),
            async_example(2),
            async_example(3),
            async_example(4),
            async_example(5),
            async_example(6),
        )


    # Run the main async function
    asyncio.run(main())

    # Log all tracked function times
    time_tracker.log_all_times()

    # 输出特定函数的执行时间
    time_tracker.log_single_time("sync_example")
    time_tracker.log_single_time("async_example")
