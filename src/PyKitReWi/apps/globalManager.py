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
    该管理器根据类对象提供单一实例，避免重复实例化类的对象，并允许在多个模块中共享同一个实例。
    如果该类的实例尚未创建，管理器将会创建并返回该实例；如果已经创建，则返回现有实例。
    """

    def __init__(self):
        # 存储已实例化的类实例的字典，键为类名，值为类的实例
        self._instances: Dict[str, object] = {}

    def get_instance(self, class_type: type, signal_sender: object, signal_receiver: Callable) -> object:
        """
        获取指定类类型的实例，并连接信号和槽。

        :param class_type: 需要实例化的类类型（类对象）
        :param signal_sender: 发送信号的对象（应该有信号机制）
        :param signal_receiver: 信号接收函数（槽函数）
        :return: 已实例化的类的对象
        """

        # 获取类名字符串
        class_name = class_type.__name__

        # 如果该类还没有实例化，则进行实例化
        if class_name not in self._instances:
            # 实例化类，并存储在字典中
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

        :param class_type: 需要实例化的类类型（类对象）
        :return: 已实例化的类的对象
        """
        # 获取类名字符串
        class_name = class_type.__name__

        # 如果该类还没有实例化，则进行实例化
        if class_name not in self._instances:
            # 实例化类，并存储在字典中
            instance = class_type()
            self._instances[class_name] = instance

        # 返回已实例化的类实例
        return self._instances[class_name]

    def save_instance(self, instance: object) -> None:
        """
        保存一个已经存在的实例到管理器中。

        :param instance: 已创建的类实例
        :return: None
        """
        class_name = instance.__class__.__name__

        # 将已经存在的实例保存到字典中
        if class_name not in self._instances:
            self._instances[class_name] = instance
