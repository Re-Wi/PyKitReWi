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
    Manages global instances, ensuring that each class has only one instance during the program's runtime
    and that instances are shared across different modules.

    This manager implements a singleton-like pattern, ensuring that a class has only one instance during the
    program’s runtime. It allows multiple modules to share the same instance. If the instance of a class has not been
    created yet, the manager instantiates and returns it. If the instance already exists, it returns the existing one.
    """

    def __init__(self) -> None:
        """
        Initializes the GlobalInstanceManager.

        This constructor initializes an internal dictionary to store instantiated objects. The dictionary's keys
        are class names, and the values are class instances.
        """
        self._instances: Dict[str, object] = {}

    def get_instance(self, class_type: type, signal_sender: object, signal_receiver: Callable) -> object:
        """
        Retrieves the instance of the specified class type and connects signals to slots.

        Args:
            class_type (type): The class type to instantiate (class object).
            signal_sender (object): The object that sends the signal (should have a signal mechanism).
            signal_receiver (Callable): The function to connect as the signal receiver (slot function).

        Returns:
            object: The instantiated class object.

        Usage:
            # Example of retrieving and connecting signals:
            instance = manager.get_instance(MyClass, signal_sender, signal_receiver)
            # This will return the instance of MyClass, and connect signal_sender to signal_receiver.
        """
        class_name = class_type.__name__

        if class_name not in self._instances:
            instance = class_type()
            self._instances[class_name] = instance

            if hasattr(signal_sender, 'connect'):
                signal_sender.connect(signal_receiver)

        return self._instances[class_name]

    def get_instance_no_signal(self, class_type: type) -> object:
        """
        Retrieves the instance of the specified class type without connecting signals and slots.

        Args:
            class_type (type): The class type to instantiate (class object).

        Returns:
            object: The instantiated class object.

        Usage:
            # Example of retrieving an instance without signal-slot connection:
            instance = manager.get_instance_no_signal(MyClass)
            # This will return the instance of MyClass, without connecting any signals.
        """
        class_name = class_type.__name__

        if class_name not in self._instances:
            instance = class_type()
            self._instances[class_name] = instance

        return self._instances[class_name]

    def save_instance(self, instance: object) -> None:
        """
        Saves an already created instance to the manager.

        Args:
            instance (object): The class instance to store in the manager.

        Returns:
            None

        Usage:
            # Example of saving an instance manually:
            manager.save_instance(my_instance)
            # This will store the given instance in the manager for future use.
        """
        class_name = instance.__class__.__name__

        if class_name not in self._instances:
            self._instances[class_name] = instance
