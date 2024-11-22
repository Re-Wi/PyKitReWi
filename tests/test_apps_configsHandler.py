import os
import unittest
from src.PyKitReWi.utils.configsHandler import ConfigsHandler


class TestConfigsHandler(unittest.TestCase):

    def setUp(self):
        """在每个测试方法之前执行，用于初始化共享的测试数据"""
        self.test_dir = 'data/config'

    def test_load_yaml_config(self):
        """测试 YAML 配置文件加载"""
        yaml_handler = ConfigsHandler(file_path=os.path.join(self.test_dir, 'conf.yaml'))

        # 进行断言，检查配置文件中的值是否正确
        self.assertEqual(yaml_handler.appname, 'MyApp')
        self.assertEqual(yaml_handler.version, 1.0)
        self.assertFalse(yaml_handler.debug)
        self.assertEqual(yaml_handler.database.host, 'localhost')
        self.assertEqual(yaml_handler.database.port, 5430)
        self.assertEqual(yaml_handler.datasRecorderTime, 1000)

    def test_load_json_config(self):
        """测试 JSON 配置文件加载"""
        json_handler = ConfigsHandler(file_path=os.path.join(self.test_dir, 'conf.json'))

        # 进行断言，检查配置文件中的值是否正确
        self.assertEqual(json_handler.appname, 'MyApp')
        self.assertEqual(json_handler.version, 1.1)
        self.assertFalse(json_handler.debug)
        self.assertEqual(json_handler.database.host, 'localhost')
        self.assertEqual(json_handler.database.port, 5431)
        self.assertEqual(json_handler.datasRecorderTime, 1000)

    def test_load_toml_config(self):
        """测试 TOML 配置文件加载"""
        toml_handler = ConfigsHandler(file_path=os.path.join(self.test_dir, 'conf.toml'))

        # 进行断言，检查配置文件中的值是否正确
        self.assertEqual(toml_handler.appname, 'MyApp')
        self.assertEqual(toml_handler.version, 1.2)
        self.assertFalse(toml_handler.debug)
        self.assertEqual(toml_handler.database.host, 'localhost')
        self.assertEqual(toml_handler.database.port, 5432)
        self.assertEqual(toml_handler.datasRecorderTime, 1000)


if __name__ == '__main__':
    # 运行所有测试
    unittest.main()
