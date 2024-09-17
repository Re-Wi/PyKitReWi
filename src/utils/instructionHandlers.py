# 导入相关模块
import json
import os


class InstructionRecorder:
    file_paths = []  # 文件列表
    file_path = './data/instruction/Project01'
    project_name = '项目1'
    configList = []
    newData = {"id": 0, "function": "功能1", "instruction": "A0 B0 C0 D0 E0", "protocol": "I2C",
               "description": "", "button": "是"}

    # 扫描文件获取信息
    def ScanDirectoryFile(self, picturesPath=''):
        # 读取文件夹文件
        self.file_paths.clear()
        for root, dirs, files in os.walk(picturesPath, topdown=False):
            for file in files:
                if file.lower().endswith(('.json',)):
                    file_path = os.path.join(root, file)
                    self.file_paths.append(file_path)
        return self.file_paths

    def OpenConfig(self, file_path):
        self.file_path = file_path
        # 读取文件数据
        with open(file_path, "r", encoding="utf-8") as f:
            jsonData = json.load(f)
        self.configList = jsonData['configList']
        # print(self.configList)

    def SaveConfig(self, context: dict, clean=False):
        if clean:
            self.configList.clear()
            return
        self.configList.append(context)

    def SaveAllConfig(self, file_path, project_name=""):
        self.file_path = file_path
        self.project_name = project_name
        context = {
            "fileName": os.path.basename(file_path),
            "projectName": project_name,
            "configList": self.configList
        }
        jsonData = json.dumps(context, ensure_ascii=False, indent=2)
        f = open(file_path, 'w', encoding='utf-8')
        f.write(jsonData)
        f.close()
