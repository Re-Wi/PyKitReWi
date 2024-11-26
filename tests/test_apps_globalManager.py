import unittest
from unittest.mock import patch
from src.PyKitReWi.apps.configsHandler import ConfigsHandler
from src.PyKitReWi.utils.example_class import ExampleCallableClass
from src.PyKitReWi.apps.globalManager import GlobalInstanceManager


def example_receiver(message: str):
    """
    示例接收函数，用于接收通过信号发出的消息。
    """
    print(f"Received message: {message}")


class TestGlobalInstanceManager(unittest.TestCase):

    def setUp(self):
        """
        在每个测试方法之前执行的初始化工作。
        """
        self.instance_manager = GlobalInstanceManager()
        self.sender = ExampleCallableClass()
        self.clss_name = ExampleCallableClass

    def test_singleton_instance(self):
        """
        测试 GlobalInstanceManager 的实例化是否为单例。
        """
        # 模拟模块 1 获取 ExampleClass 的实例
        instance1 = self.instance_manager.get_instance(self.clss_name, self.sender, example_receiver)

        # 模拟模块 2 获取 ExampleClass 的实例，应该返回相同的实例
        instance2 = self.instance_manager.get_instance(self.clss_name, self.sender, example_receiver)

        # 验证两个实例是否是同一个实例
        self.assertIs(instance1, instance2, "The instances should be the same.")

    def test_signal_and_slot(self):
        """
        测试信号和槽机制是否正确工作。
        """
        # 发送信号
        self.sender.emit("Hello from sender!")

        # 验证信号是否成功传递，输出应被打印
        # (你可以在测试中捕获输出并断言，而不是直接输出到终端)

    def test_config_instance(self):
        """
        测试配置文件的实例化与共享。
        """
        configHandler = ConfigsHandler(file_path='../data/config/conf.yaml')

        # 保存实例
        self.instance_manager.save_instance(configHandler)

        # 获取配置实例，应该返回相同的实例
        instance3 = self.instance_manager.get_instance_no_signal(ConfigsHandler)

        # 验证两个配置实例是否是同一个实例
        self.assertIs(instance3, self.instance_manager.get_instance_no_signal(ConfigsHandler),
                      "The ConfigHandler instances should be the same.")

        # 打印配置版本
        myConfig = instance3.configs
        print(f'{__name__} get config Version', myConfig.version)


if __name__ == '__main__':
    unittest.main()
