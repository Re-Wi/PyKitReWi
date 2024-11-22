# -*- coding: UTF-8 -*-
"""
@Project    : PyKitReWi
@File       : debugHelper.py
@IDE        : PyCharm
@Author     : ReWi  # 替换为当前系统用户名（方便开发人员区分）
@Date       : 2024/11/22 23:02  # 日期和时间精确到秒
@License    : MIT
@Contact    : RejoiceWindow <RejoiceWindow@yeah.net>
@Description: 开发软件调试时使用，如：追踪程序运行时间
@Version    : v0.0.0
@Dependencies: 
    - contextlib
    - time
    - asyncio
    - typing
    - functools
    - loguru
@Changelog  : 
    - v0.0.0 (2024/11/22 23:02): Initial version, implemented the core functionality.
    - v0.0.1 (2024/11/22 23:02)  # 记录文件版本更新的日志，例如修复的bug、增加的功能等
"""
from contextlib import contextmanager
import time
import asyncio
from typing import Callable, Any, Dict, List
from functools import wraps
from loguru import logger


class TimeTracker:
    def __init__(self, max_count: int = 6):
        """
        Initialize a TimeTracker instance that stores execution times for multiple functions.

        Args:
            max_count (int): Maximum number of execution times to track for each function.
                             Once the limit is reached, older entries are discarded.

        Attributes:
            times (dict): A dictionary where keys are function names (str) and values are lists of execution times (float).
            max_count (int): The maximum number of entries to keep for each function.
        """
        self.times: Dict[str, List[float]] = {}
        self.max_count = max_count

    def track_time(self, func: Callable) -> Callable:
        """
        Decorator function that wraps a given function (synchronous or asynchronous)
        and tracks its execution time.

        Args:
            func (Callable): The function whose execution time is to be tracked.

        Returns:
            Callable: The wrapped function with time-tracking functionality.
        """

        @wraps(func)
        async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
            """Wrapper for asynchronous functions."""
            start_time = self.get_start_time()

            # Execute the original function asynchronously
            result = await func(*args, **kwargs)

            exec_time = self.get_exec_time(func.__name__, start_time)
            return result

        @wraps(func)
        def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
            """Wrapper for synchronous functions."""
            start_time = self.get_start_time()

            # Execute the original function
            result = func(*args, **kwargs)

            exec_time = self.get_exec_time(func.__name__, start_time)
            return result

        # Return async wrapper if the function is asynchronous, otherwise return sync wrapper
        return async_wrapper if asyncio.iscoroutinefunction(func) else sync_wrapper

    def get_start_time(self) -> (float, str):
        """
        Get the current time and a formatted timestamp.

        Returns:
            float: The start time in seconds.
            str: Formatted timestamp.
        """
        start_time = time.time()
        # start_timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(start_time))
        return start_time  # , start_timestamp

    def get_exec_time(self, func_name: str, start_time: float) -> float:
        """
        Calculate execution time and store it in the times dictionary.

        Args:
            func_name (str): The name of the function being tracked.
            start_time (float): The start time in seconds.

        Returns:
            float: The execution time.
        """
        end_time = time.time()
        exec_time = end_time - start_time

        # Log the execution time
        logger.info(f"[{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(start_time))}] "
                    f"{func_name} took {exec_time:.6f} seconds to execute")

        # Store the execution time, ensuring the max count is respected
        self._store_time(func_name, exec_time)
        return exec_time

    def _store_time(self, func_name: str, exec_time: float) -> None:
        """
        Store the execution time in the times dictionary, respecting the max_count limit.

        Args:
            func_name (str): The name of the function whose execution time is being tracked.
            exec_time (float): The execution time in seconds.
        """
        if func_name not in self.times:
            self.times[func_name] = []
        self.times[func_name].append(exec_time)
        if len(self.times[func_name]) > self.max_count:
            # Remove the oldest execution time if the limit is exceeded
            self.times[func_name].pop(0)

    def log_all_times(self, title="Execution") -> None:
        """
        Logs the total and average execution times for all tracked functions.
        """
        logger.info(f"~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ {title} --> Summary ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        for func_name, exec_times in self.times.items():
            total_time = sum(exec_times)
            avg_time = total_time / len(exec_times)
            logger.info(
                f"Function: {func_name: <20} \t| Total Time: {total_time:.6f}s \t| Average Time: {avg_time:.6f}s")
        logger.info("=================================================================================================")

    def log_single_time(self, label_name: str) -> None:
        """
        Logs the total and average execution time for a specific function.

        Args:
            label_name (str): The name of the function whose execution times are to be logged.
        """
        if label_name in self.times:
            exec_times = self.times[label_name]
            total_time = sum(exec_times)
            avg_time = total_time / len(exec_times)
            logger.info(
                f"Function: {label_name: <20} \t| Total Time: {total_time:.6f}s \t| Average Time: {avg_time:.6f}s")
        else:
            logger.warning(f"No data found for function: {label_name}")

    def get_total_time(self, label_name: str) -> float:
        """
        Retrieves the total execution time for a specific function.

        Args:
            label_name (str): The name of the function whose execution times are to be retrieved.

        Returns:
            float: The total execution time for the function. Returns 0 if no data is found.
        """
        if label_name in self.times:
            exec_times = self.times[label_name]
            total_time = sum(exec_times)  # 计算总时间
            return total_time
        else:
            logger.warning(f"No data found for function: {label_name}")
            return 0.0  # 如果没有找到数据，返回 0

    @contextmanager
    def time_code_block(self, label: str):
        """
        Context manager to simplify tracking execution time of code blocks.

        Args:
            label (str): Label for the code block.

        Usage:
            with tracker.time_code_block("block_name"):
                # Code block
        """
        start_time = self.get_start_time()
        try:
            yield
        finally:
            exec_time = self.get_exec_time(label, start_time)
