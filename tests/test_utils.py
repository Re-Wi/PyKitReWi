import time

from PySide6.QtCore import Signal

from src.utils.debugHelper import TimeTracker


class UtilsExample:
    # 声明带一个字典类型参数的信号
    mainSignal = Signal(dict)  # 主界面的信号用来绑定子界面类的函数方法

    def __init__(self):
        # 引入公共程序
        from src.utils.common import commonProgram
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


tracker = TimeTracker()


@tracker.track_time
def example_function(x: int) -> None:
    """
    Example function that sleeps for x seconds to simulate work.

    Args:
        x (int): Number of seconds to sleep.
    """
    time.sleep(x)


@tracker.track_time
def another_function(y: float) -> None:
    """
    Another example function that sleeps for y seconds to simulate work.

    Args:
        y (float): Number of seconds to sleep.
    """
    time.sleep(y)


if __name__ == "__main__":
    # Simulate calling the functions multiple times
    example_function(1)
    example_function(2)
    another_function(1.5)
    another_function(2.5)

    # Log execution time for a specific function
    tracker.log_single_time("example_function")

    # Log execution time summary for all tracked functions
    tracker.log_all_times()
