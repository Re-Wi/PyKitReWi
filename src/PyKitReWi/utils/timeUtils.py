# -*- coding: UTF-8 -*-
"""
@Project    : PyKitReWi
@File       : timeUtils.py
@IDE        : PyCharm
@Author     : ReWi  # 替换为当前系统用户名（方便开发人员区分）
@Date       : 2024/11/27 8:45  # 日期和时间精确到秒
@License    : MIT
@Contact    : RejoiceWindow <RejoiceWindow@yeah.net>
@Description: 时间控制相关
@Version    : v0.0.0
@Dependencies: 
    - python3
@Changelog  : 
    - v0.0.0 (2024/11/27 8:45): Initial version, implemented the core functionality.
    - v0.0.1 (2024/11/27 8:45)  # 记录文件版本更新的日志，例如修复的bug、增加的功能等
"""
import time


def DelaySeconds(seconds: float) -> None:
    """
    延时指定的秒数。

    使用 time.perf_counter() 作为高精度计时器，计算经过的时间，并通过循环实现延时。此方法适用于需要精确到秒级的延时操作。

    Args:
        seconds (float): 要延迟的秒数，可以是浮动的数字，例如 1.5 秒或 0.002 秒。

    Returns:
        None: 该函数通过时间循环来实现延迟，不返回任何值。

    Usage:
        DelaySeconds(2.5)  # 延时 2.5 秒
    """
    # 获取当前时间作为开始时间
    start_time = time.perf_counter()

    # 循环直到经过的时间大于或等于指定的秒数
    while time.perf_counter() - start_time < seconds:
        pass


def DelayMilliseconds(milliseconds: float) -> None:
    """
    延时指定的毫秒数。

    通过调用 DelaySeconds() 方法来实现毫秒级的延时。将毫秒数转换为秒，然后进行延时。

    Args:
        milliseconds (float): 要延迟的毫秒数，可以是浮动的数字，例如 150 毫秒或 0.5 毫秒。

    Returns:
        None: 该函数不返回任何值，直接通过秒延迟实现毫秒级延时。

    Usage:
        DelayMilliseconds(100)  # 延时 100 毫秒
    """
    # 将毫秒转换为秒，然后调用 DelaySeconds 实现延时
    DelaySeconds(milliseconds / 1000)


def DelayMicroseconds(microseconds: float) -> None:
    """
    延时指定的微秒数。

    通过调用 DelaySeconds() 方法来实现微秒级的延时。将微秒数转换为秒后进行延时。

    Args:
        microseconds (float): 要延迟的微秒数，可以是浮动的数字，例如 1000 微秒或 0.0005 微秒。

    Returns:
        None: 该函数不返回任何值，直接通过秒延迟实现微秒级延时。

    Usage:
        DelayMicroseconds(1000)  # 延时 1000 微秒（即 1 毫秒）
    """
    # 将微秒转换为秒，然后调用 DelaySeconds 实现延时
    DelaySeconds(microseconds / 1_000_000)


def DelayNanoseconds(nanoseconds: float) -> None:
    """
    延时指定的纳秒数。

    通过调用 DelaySeconds() 方法来实现纳秒级的延时。将纳秒数转换为秒后进行延时。

    Args:
        nanoseconds (float): 要延迟的纳秒数，可以是浮动的数字，例如 1000000 纳秒或 0.5 纳秒。

    Returns:
        None: 该函数不返回任何值，直接通过秒延迟实现纳秒级延时。

    Usage:
        DelayNanoseconds(1000000)  # 延时 1000000 纳秒（即 1 毫秒）
    """
    # 将纳秒转换为秒，然后调用 DelaySeconds 实现延时
    DelaySeconds(nanoseconds / 1_000_000_000)
