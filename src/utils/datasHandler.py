# 导入相关模块
import json
import os
from datetime import datetime

import pytz
from PySide6.QtCore import QMutex, QThread
from jinja2 import Template, FileSystemLoader, Environment

# 首先告诉Jinja2模块，jinja模板文件路径在哪？(如当前目录)
# j2_loader = FileSystemLoader('./')
# 然后定义一个环境，告诉jinja2，从哪里调用模板
# env = Environment(loader=j2_loader)
# 之后通过 get_template 获取并载入模板
# j2_tmpl = env.get_template('./jinja2.j2')
# 最后传入参数，渲染模板
# result = j2_tmpl.render(name="xdai")
# print(result)

# 配置jinja模板
from utils.filePathHelper import EnsureFolders

template_path = os.path.join(os.path.dirname(__file__), "../data/template")
jinja_env = Environment(
    loader=FileSystemLoader(template_path), autoescape=True
)


class DatasSaver:
    def InitPathEnv(self, templateDir='data/template'):
        global template_path
        global jinja_env
        template_path = os.path.join('./', templateDir)
        jinja_env = Environment(
            loader=FileSystemLoader(template_path), autoescape=True
        )

    def LogSave(self, dst, data):
        with open(dst, 'w', encoding='utf-8') as fp:
            fp.write(data)

    # 渲染模板，与werkzueg结合可以返回一个Response
    # 这个例子将渲染好的html页面输出到文件out.html
    def render_template(self, file_path, file_name, **context):
        jsonData = json.dumps(context, ensure_ascii=False, indent=2)
        t = jinja_env.get_template('template.html')
        # t.render(context) 返回一个str字符串
        data = t.render(context)
        self.LogSave(file_path + file_name + '.html', data)
        f2 = open(file_path + file_name + '.json', 'w', encoding='utf-8')
        f2.write(jsonData)
        f2.close()


class DatasRecorder:
    testList = []
    inputId = 0
    inputList = []
    itemId = 0
    itemList = []
    imageId = 0
    imageList = []
    statusId = 0
    statusList = []
    versionId = 0
    versionList = []
    dtcId = 0
    dtcList = []
    file_path = 'data/records/'
    file_name = 'index'

    # 使用 __init__ 初始化数据 的话，使用一次 LogsRecorder() 会执行一次，如：type(LogsRecorder())
    def InitFile(self, file_name: str = 'index', templateDir='data/template'):
        if len(file_name.strip()) > 0:
            self.file_name = file_name
        # "%Y-%m-%d %H:%M:%S.%f
        # 指定Tokyo时区当前时间
        timeStr = datetime.now(pytz.timezone('Asia/Shanghai')).strftime("%Y-%m-%d_%H-%M")
        self.file_path = EnsureFolders('data/records/' + timeStr + '/')
        self.logsSaver = DatasSaver()
        self.logsSaver.InitPathEnv(templateDir=templateDir)

    def InputFun(self, dictData: dict):
        timeStr = datetime.now(pytz.timezone('Asia/Shanghai')).strftime("%Y-%m-%d %H:%M:%S.%f")
        inputObj = {"id": self.inputId, "key": dictData['key'], "rot": dictData['rot'],
                    "type": dictData.get('type', '-'), "time": timeStr}
        self.inputId += 1
        self.inputList.append(inputObj)

    def ItemFun(self, dictData: dict):
        timeStr = datetime.now(pytz.timezone('Asia/Shanghai')).strftime("%Y-%m-%d %H:%M:%S.%f")
        itemObj = {"id": self.itemId, "index": dictData['index'], "itemName": dictData['itemName'],
                   "objPrefix": dictData['objPrefix'], "time": timeStr}
        self.itemId += 1
        self.itemList.append(itemObj)

    def ImageFun(self, dictData: dict):
        timeStr = datetime.now(pytz.timezone('Asia/Shanghai')).strftime("%Y-%m-%d %H:%M:%S.%f")
        imageObj = {"id": self.imageId, "index": dictData['index'], "file": dictData['file'], "time": timeStr}
        self.imageId += 1
        self.imageList.append(imageObj)

    def StatusFun(self, objData):
        timeStr = datetime.now(pytz.timezone('Asia/Shanghai')).strftime("%Y-%m-%d %H:%M:%S.%f")
        statusObj = {"id": self.statusId, "onoff": objData.onoff, "light": objData.light,
                     "module_temp": objData.module_temp, "voltage": objData.voltage, "current": objData.current,
                     "power": objData.power, "pcb_temp": objData.pcb_temp, "gyro": objData.gyro, "time": timeStr}
        self.statusId += 1
        self.statusList.append(statusObj)

    def VersionFun(self, objData):
        timeStr = datetime.now(pytz.timezone('Asia/Shanghai')).strftime("%Y-%m-%d %H:%M:%S.%f")
        versionObj = {"id": self.versionId, "hw": objData.hw, "sw": objData.sw, "boot": objData.boot,
                      "time": timeStr}
        self.versionId += 1
        self.versionList.append(versionObj)

    def DTCFun(self, objData):
        timeStr = datetime.now(pytz.timezone('Asia/Shanghai')).strftime("%Y-%m-%d %H:%M:%S.%f")
        dtcObj = {"id": self.dtcId, "prefix": objData.prefix, "value": objData.value, "time": timeStr}
        self.dtcId += 1
        self.dtcList.append(dtcObj)

    def SaveAllRecorder(self):
        context = {
            "testList": self.testList,
            "inputList": self.inputList,
            "itemList": self.itemList,
            "imageList": self.imageList,
            "statusList": self.statusList,
            "versionList": self.versionList,
            "dtcList": self.dtcList,
        }
        self.logsSaver.render_template(file_path=self.file_path, file_name=self.file_name, **context)


qmutSaveLog = QMutex()  # 创建线程锁


# 继承QThread
class SaveLogRunthread(QThread):
    # 创建指针
    datasRecorder = DatasRecorder()

    def __init__(self):
        super(SaveLogRunthread, self).__init__()

    def __del__(self):
        try:
            self.wait()
        except Exception as err:
            pass

    def run(self):
        # print('SaveLogRunthread 1')
        qmutSaveLog.lock()  # 加锁
        # print('SaveLogRunthread 2')
        try:
            # print('SaveLogRunthread 3')
            self.datasRecorder.SaveAllRecorder()
            # print('SaveLogRunthread 4')
            qmutSaveLog.unlock()  # 解锁
        except Exception as err:
            qmutSaveLog.unlock()  # 解锁
            print('Save datas Runthread ERROR :', err)
