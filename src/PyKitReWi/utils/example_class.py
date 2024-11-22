# -*- coding: UTF-8 -*-
"""
@Project    : PyKitReWi
@File       : example_class.py.py
@IDE        : PyCharm
@Author     : ReWi  # 替换为当前系统用户名（方便开发人员区分）
@Date       : 2024/11/22 16:52  # 日期和时间精确到秒
@License    : MIT
@Contact    : RejoiceWindow <RejoiceWindow@yeah.net>
@Description: 示例类
@Version    : v0.0.0
@Dependencies: 
    - python3
@Changelog  : 
    - v0.0.0 (2024/11/22 16:52): Initial version, implemented the core functionality.
    - v0.0.1 (2024/11/22 16:52)  # 记录文件版本更新的日志，例如修复的bug、增加的功能等
"""

from typing import Callable, Dict


class ExampleCallableClass:
    """
    示例类，包含信号和槽，用于演示如何与 GlobalInstanceManager 交互。

    这里只定义了一个简单的信号机制，使用 Python 内建的信号与槽方式。
    """

    def __init__(self):
        self._listeners = []  # 用于存储所有的槽函数
        print(f"{self.__class__.__name__} instance created.")  # 类实例化时打印消息

    def connect(self, listener: Callable):
        """连接信号到槽函数"""
        self._listeners.append(listener)

    def emit(self, *args, **kwargs):
        """触发信号，调用所有连接的槽函数"""
        for listener in self._listeners:
            listener(*args, **kwargs)
