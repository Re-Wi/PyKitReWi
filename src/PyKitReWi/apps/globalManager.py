# -*- coding: UTF-8 -*-
"""
@Project    : PyKitReWi
@File       : globalManager.py
@IDE        : PyCharm
@Author     : ReWi  # 替换为当前系统用户名（方便开发人员区分）
@Date       : 2024/11/22 16:50  # 日期和时间精确到秒
@License    : MIT
@Contact    : RejoiceWindow <RejoiceWindow@yeah.net>
@Description:   # 这里可以填写简短的文件功能描述
@Version    : v0.0.0
@Dependencies: 
    - python3
@Changelog  : 
    - v0.0.0 (2024/11/22 16:50): Initial version, implemented the core functionality.
    - v0.0.1 (2024/11/22 16:50)  # 记录文件版本更新的日志，例如修复的bug、增加的功能等
"""
from typing import Callable, Dict


class GlobalInstanceManager:
    """
    管理全局范围内的实例，确保每个类在程序运行期间只有一个实例，并且在不同模块之间共享这些实例。

    This manager provides a singleton-like pattern, ensuring that each class has only one instance
    throughout the program's runtime and that these instances are shared across different modules.

    该管理器提供类似单例模式的功能，根据类类型创建并返回该类的单一实例，避免重复实例化对象。
    它允许多个模块共享同一个实例。如果该类的实例尚未创建，管理器将会实例化并返回该实例；
    如果已创建，则返回现有的实例。
    """

    def __init__(self) -> None:
        """
        初始化 GlobalInstanceManager。

        Initializes the GlobalInstanceManager.

        该构造函数初始化了一个字典，用于存储已实例化的对象。字典的键是类名，值是类实例。
        This constructor sets up the internal dictionary to store instantiated objects.
        The dictionary's keys are class names, and the values are class instances.
        """
        self._instances: Dict[str, object] = {}

    def get_instance(self, class_type: type, signal_sender: object, signal_receiver: Callable) -> object:
        """
        获取指定类类型的实例，并连接信号和槽。

        Retrieves the instance of the specified class type and connects signals to slots.

        :param class_type: 需要实例化的类类型（类对象）。
        :param class_type: The class type to instantiate (class object).

        :param signal_sender: 发送信号的对象（应该有信号机制）。
        :param signal_sender: The object that sends the signal (should have a signal mechanism).

        :param signal_receiver: 连接的信号接收函数（槽函数）。
        :param signal_receiver: The function to connect as the signal receiver (slot function).

        :return: 已实例化的类对象。
        :return: The instantiated class object.
        """
        # 获取类名字符串
        class_name = class_type.__name__

        # 如果该类还没有实例化，则进行实例化
        if class_name not in self._instances:
            # 实例化类并存储在字典中
            instance = class_type()
            self._instances[class_name] = instance

            # 连接信号和槽
            if hasattr(signal_sender, 'connect'):
                signal_sender.connect(signal_receiver)

        # 返回已实例化的类实例
        return self._instances[class_name]

    def get_instance_no_signal(self, class_type: type) -> object:
        """
        获取指定类类型的实例，且不涉及信号和槽的连接。

        Retrieves the instance of the specified class type without connecting signals and slots.

        :param class_type: 需要实例化的类类型（类对象）。
        :param class_type: The class type to instantiate (class object).

        :return: 已实例化的类对象。
        :return: The instantiated class object.
        """
        # 获取类名字符串
        class_name = class_type.__name__

        # 如果该类还没有实例化，则进行实例化
        if class_name not in self._instances:
            # 实例化类并存储在字典中
            instance = class_type()
            self._instances[class_name] = instance

        # 返回已实例化的类实例
        return self._instances[class_name]

    def save_instance(self, instance: object) -> None:
        """
        将已创建的实例保存到管理器中。

        Saves an already created instance to the manager.

        :param instance: 已创建的类实例。
        :param instance: The class instance to store in the manager.

        :return: 空
        :return: None
        """
        class_name = instance.__class__.__name__

        # 如果字典中没有该实例，则将其保存
        if class_name not in self._instances:
            self._instances[class_name] = instance
