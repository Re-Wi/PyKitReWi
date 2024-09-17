import os
import yaml
import argparse
from .configsDefault import DEFAULT_CONFIG


def Dict2Namespace(namespace, config):
    if namespace is None:
        namespace = argparse.Namespace()
    for key, value in config.items():
        if isinstance(value, dict):
            new_value = Dict2Namespace(getattr(namespace, key, None), value)
        else:
            new_value = value
        setattr(namespace, key, new_value)

    return namespace


class ConfigsHandler:
    """
    加载全局配置
    """
    configs = None
    file_path = 'data/config/yaml/conf.yaml'
    # 创建一个空的命名空间对象
    namespace = argparse.Namespace()

    def LoadData(self, file_path=""):
        """
        使用 __init__ 初始化数据 的话，使用一次 ConfigHandler() 会执行一次，如：type(ConfigHandler())
        :param file_path:
        :return:
        """
        if len(file_path) > 1:
            self.file_path = file_path
        pathConfig = os.path.join(self.file_path)
        if not os.path.exists(pathConfig):
            print(f'Folder {pathConfig} not exists')
            print("Manually create global variables in the Python file.")
            self.configs = Dict2Namespace(self.namespace, DEFAULT_CONFIG)
            return self.configs
        self.MakeArgs(self.file_path)
        # print(self.configs)
        self.LoadExtYamlFiles()
        return self.configs

    def LoadExtYamlFiles(self):
        # Check and load additional YAML files from ExtYamlFiles field
        try:
            if len(self.configs.ExtYamlFiles) > 0:
                for ext_yaml_file in self.configs.ExtYamlFiles:
                    ext_yaml_path = os.path.join(self.configs.configDir, ext_yaml_file)
                    if os.path.exists(ext_yaml_path):
                        self.MakeArgs(ext_yaml_path)
                    else:
                        print(f'Warning: File {ext_yaml_file} not found. It will be skipped.')
        except Exception as err:
            print(err)

    def MakeArgs(self, fileDir):
        # Load and merge main config file
        # 1.创建解释器
        parser = argparse.ArgumentParser(description="可写可不写，只是在命令行参数出现错误的时候，随着错误信息打印出来。")
        # 2.添加需要的参数
        parser.add_argument('--cfg', type=str, default=fileDir, help="...")
        # 3.进行参数解析
        args = parser.parse_args()
        filepath = args.cfg
        with open(filepath, 'r', encoding='utf-8') as f:
            config = yaml.load(f, Loader=yaml.FullLoader)
        self.configs = Dict2Namespace(self.namespace, {**config, **vars(args)})


# configHandler = ConfigHandler()
# 程序入口
if __name__ == '__main__':
    configHandler = ConfigsHandler()
    configHandler.LoadData(file_path='../data/config/conf.yaml')
    # print(globals().get('configs'))
    print(configHandler.configs)
    print(configHandler.configs.ExtYamlFiles)
    print(configHandler.configs.testItems)
