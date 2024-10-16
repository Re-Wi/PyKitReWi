# encoding: utf-8
import sys


class CommonProgram:
    """
    CommonProgram() , a program that is called repeatedly by multiple programs
    公用程序，会被多个程序多次重复调用的程序
    """
    __myConfig = None
    __time_tracker = None
    __serialPortWin = None
    __logsRecorder = None
    __datasRecorder = None
    __configHandler = None
    __sqlite3Handler = None
    __ft4222Win = None

    def __init__(self):  # As a prompt to create the object
        print('The CommonProgram is created successfully. Select components in each window as required')

    def EnableConfigHandler(self):  # 启用全局配置信息
        from utils.configsHandler import ConfigsHandler
        """ Enable global configuration information """
        if type(self.__configHandler) != type(ConfigsHandler()):
            self.__configHandler = ConfigsHandler()
            print('Create ConfigHandler')
            ## 加载配置文件
            self.__myConfig = self.__configHandler.LoadData(file_path='./data/config/conf.yaml')
            # 初始化测试项
            self.__myConfig.passTestItems = set()
            print('get config Version', self.__myConfig.version)
        return self.__myConfig

    def EnableTimeTracker(self):  # 启用 函数运行统计 模块
        """
        Enable the Time Tracker module
        """
        from utils.debugHelper import TimeTracker
        if type(self.__time_tracker) != type(TimeTracker()):
            self.__time_tracker = TimeTracker()
        return self.__time_tracker

    def UpdateScreenResolution(self):  # 更新全局配置中显示器分辨率
        """ Updated the monitor resolution in Global configuration """
        self.EnableConfigHandler()
        try:
            from PySide6.QtCore import Qt
            from PySide6.QtWidgets import QApplication
            # 获取显示器分辨率
            self.desktop = QApplication.desktop()
            if not self.desktop:
                app = QApplication(sys.argv)
                self.desktop = QApplication.desktop()
            self.screenRect = self.desktop.screenGeometry()
            self.screen_height = self.screenRect.height()
            self.screen_width = self.screenRect.width()
            self.screen_ratio = self.desktop.devicePixelRatio()
            self.screen_resolution = str(self.screen_width * self.screen_ratio) + 'x' + str(
                self.screen_height * self.screen_ratio)
            print("Screen height {}".format(self.screen_height))
            print("Screen width {}".format(self.screen_width))
            print("Screen ratio {}".format(self.screen_ratio))
            # 修改分辨率
            self.__myConfig.screenLength = self.screen_width
            self.__myConfig.screenWidth = self.screen_height
            self.__myConfig.screenRatio = self.screen_ratio
            self.__myConfig.screenResolution = self.screen_resolution
        except Exception as err:
            print('UpdateScreenResolution ERROR:', err)
            return False
        return True

    def UpdatePicturesPath(self):  # 更新全局配置中图片路径
        """ Update the image path in the global configuration """
        self.EnableConfigHandler()
        # 确定图片路径
        rootPath = self.__myConfig.picturesRootPath
        for item in os.scandir(rootPath):
            if item.is_dir():
                if item.name == self.__myConfig.screenResolution:
                    self.__myConfig.testPicturesPath = rootPath + self.__myConfig.screenResolution + '/'
        return self.__myConfig.testPicturesPath

    def EnableSerialPort(self, winSignal=None, RecvSerialData=None):  # 启用可控串口信息窗口模块
        """
        Enable the controllable serial port information window module
        winSignal 是窗口创建的 字典 信号，类型：Signal ，例如：mainSignal = Signal(dict)
        RecvSerialData 是窗口接收数据的 带字典参数 的函数，类型：function ，列如：def RecvSerialData(self, dictData: dict): -> None
        """
        try:
            from PySide6.QtWidgets import QApplication
            from serialPort import SerialPortWindow
            # 判断是否存在屏幕
            self.desktop = QApplication.desktop()
            if not self.desktop:
                app = QApplication(sys.argv)
                self.desktop = QApplication.desktop()
            if type(self.__serialPortWin) != type(SerialPortWindow()):
                self.__serialPortWin = SerialPortWindow()
                print('Create SerialPortWindow')
            # self.__serialPortWin.show()
            if RecvSerialData:
                # 将form2的信号_singal_2和主界面的getData_F2连接
                self.__serialPortWin.serialPortSignal.connect(RecvSerialData)
            if winSignal:
                # 将自己的信号和Form2的接受函数绑定
                winSignal.connect(self.__serialPortWin.RecvSignalData)
        except Exception as err:
            print('UpdateScreenResolution ERROR:', err)
            return None
        return self.__serialPortWin

    def EnableDatasRecorder(self, file_name: str = "index"):  # 启用数据记录模块
        """
        Enable the data logging module
        参数是保存记录的文件名（不包括后缀）
        """
        from utils.datasHandler import DatasRecorder
        if type(self.__datasRecorder) != type(DatasRecorder()):
            from PySide6.QtCore import QTimer
            self.__datasRecorder = DatasRecorder()
            self.__datasRecorder.InitFile(file_name=file_name)
            print('Create DatasRecorders')
            # 定时保存测试记录，周期为 XXXms
            self.timer_datasRecorder_delay = self.__myConfig.datasRecorderTime
            self.timer_datasRecorder = QTimer()
            self.timer_datasRecorder.timeout.connect(self.__DatasRecorderFun)
            self.timer_datasRecorder.start(self.timer_datasRecorder_delay)
        return self.__datasRecorder

    def __DatasRecorderFun(self):
        """
        测试数据定时器使用，
        只需要本对象调用一次，
        尝试调用内部方法会导致AttributeError。
        :return:
        """
        from utils.datasHandler import SaveLogRunthread
        self.timer_datasRecorder.stop()
        # 测试记录，更新测试通过项
        for test in self.__datasRecorder.testList:
            for item in self.__myConfig.passTestItems:
                if test.get('objPrefix', 'x_x') in item:
                    test.update({"result": True})
                    break
        # 创建线程
        self.saveLogRunthread = SaveLogRunthread()
        # 连接信号
        self.saveLogRunthread.datasRecorder = self.__datasRecorder
        # 开始线程
        self.saveLogRunthread.start()
        self.timer_datasRecorder.start(self.timer_datasRecorder_delay)

    def EnableLogsRecorder(self, directory="", filename: str = ""):  # 启用数据记录模块
        """
        Enable the data logging module
        参数是保存记录的文件名（包括后缀）
        :param directory:
        :param filename:
        :return:
        """
        from utils.logsRecorder import LogsRecorder
        if type(self.__logsRecorder) != type(LogsRecorder()):
            self.__logsRecorder = LogsRecorder()
            self.__logsRecorder.InitLogger(log_dir=directory, log_name=filename)
            print('Create LogsRecorder')
        return self.__logsRecorder

    def EnableSqlite3Handler(self, db_path='', db_name='BoevxaDb.db'):  # 启用数据记录模块
        """
        Enable the Sqlite3Handler module
        参数是保存记录的文件名（不包括后缀）
        """
        from utils.sqlite3Handler import Sqlite3Handler
        if type(self.__sqlite3Handler) != type(Sqlite3Handler()):
            self.__sqlite3Handler = Sqlite3Handler()
            self.__sqlite3Handler.InitSqlite3(db_path=db_path, db_name=db_name)
            print('Create Sqlite3Handler')
        return self.__sqlite3Handler

    def EnableFt4222(self, winSignal=None, RecvFt4222Data=None):  # 启用可控串口信息窗口模块
        """
        Enable the controllable serial port information window module
        winSignal 是窗口创建的 字典 信号，类型：Signal ，例如：mainSignal = Signal(dict)
        RecvSerialData 是窗口接收数据的 带字典参数 的函数，类型：function ，列如：def RecvSerialData(self, dictData: dict): -> None
        """
        try:
            from PySide6.QtWidgets import QApplication
            from ft4222Dev.ft4222Window import Ft4222Window
            # 判断是否存在屏幕
            self.desktop = QApplication.primaryScreen()
            if not self.desktop:
                app = QApplication(sys.argv)
                self.desktop = QApplication.primaryScreen()
            if type(self.__ft4222Win) != type(Ft4222Window()):
                self.__ft4222Win = Ft4222Window()
                print('Create SerialPortWindow')
            # self.__serialPortWin.show()
            if RecvFt4222Data:
                # 将form2的信号_singal_2和主界面的getData_F2连接
                self.__ft4222Win.ft4222Signal.connect(RecvFt4222Data)
            if winSignal:
                # 将自己的信号和Form2的接受函数绑定
                winSignal.connect(self.__ft4222Win.RecvSignalData)
        except Exception as err:
            print('EnableFt422 ERROR:', err)
            return None
        return self.__ft4222Win


######################################################################################
# 开发阶段才生效的代码
DEVELOP = True
# 指定 assets 文件夹的路径
ASSETS_DIR = './'
RESOURCES_DIR = 'resources'
if DEVELOP:
    from utils import resourcesCodeFix

    # 执行修改代码的程序
    resourcesCodeFix.FixErrorLine(assets_folder=ASSETS_DIR, resources_folder=RESOURCES_DIR)
######################################################################################
commonProgram = CommonProgram()

if __name__ == "__main__":
    from PySide6.QtWidgets import QApplication
    from serialPort import SerialPortWindow

    # app = QApplication(sys.argv)
    # print('__myConfig\t-->', commonProgram.__myConfig)
    print('EnableConfigHandler()\t-->', commonProgram.EnableConfigHandler())
    print('UpdateScreenResolution()\t-->', commonProgram.UpdateScreenResolution())
    # print('UpdatePicturesPath()\t-->', commonProgram.UpdatePicturesPath())
    # print('EnableSerialPort()\t-->', commonProgram.EnableSerialPort())
    # print('EnableLogsRecorder()\t-->', commonProgram.EnableLogsRecorder())
    # sys.exit(app.exec_())
