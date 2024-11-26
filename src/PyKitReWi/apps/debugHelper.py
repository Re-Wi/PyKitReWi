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
    """
    A class to track execution times of multiple functions and provide performance statistics.

    This class allows you to track the execution time of both synchronous and asynchronous functions.
    It also stores execution times in a dictionary, logs the times, and provides summary reports.

    Attributes:
        times (dict): A dictionary where keys are function names (str) and values are lists of execution times (float).
        max_count (int): The maximum number of execution times to store per function. Older entries are discarded once the limit is reached.
    """

    def __init__(self, max_count: int = 6) -> None:
        """
        Initializes the TimeTracker instance.

        Args:
            max_count (int): The maximum number of execution times to store per function. Default is 6.
                             If the limit is exceeded, older execution times are discarded.

        Attributes:
            times (dict): Stores execution times for each tracked function.
            max_count (int): Maximum number of entries to store per function.
        """
        self.times: Dict[str, List[float]] = {}
        self.max_count = max_count

    def track_time(self, func: Callable) -> Callable:
        """
        A decorator that tracks the execution time of a function (either synchronous or asynchronous).

        This decorator wraps the given function and records its execution time. It works with both
        synchronous and asynchronous functions.

        Args:
            func (Callable): The function whose execution time will be tracked.

        Returns:
            Callable: The wrapped function with time-tracking functionality.

        Usage:
            @tracker.track_time
            def some_function():
                # Function code to be executed
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

    def get_start_time(self) -> float:
        """
        Get the current time in seconds since the epoch with high precision, which will be used to calculate execution time.

        Returns:
        float: The start time in seconds with microsecond precision.

        Usage:
            start_time = tracker.get_start_time()
            # Use start_time to calculate the execution time of a function or code block
            tracker.get_exec_time("label_name", start_time)
        """
        start_time = time.perf_counter()  # High-precision timer
        # Get the time in seconds and format it to include microseconds
        local_time = time.localtime(start_time)
        formatted_time = time.strftime('%Y-%m-%d %H:%M:%S', local_time) + f".{int((start_time % 1) * 1_000_000):06d}"

        # Log the start time with full precision
        logger.debug(f"Start time: {formatted_time} (Epoch time: {start_time:.6f} seconds)")
        return start_time

    def get_exec_time(self, func_name: str, start_time: float) -> float:
        """
        Calculate and log the execution time of a function with microsecond precision.

        Args:
            func_name (str): The name of the function whose execution time is being tracked.
            start_time (float): The timestamp when the function started executing.

        Returns:
            float: The execution time in seconds, including microsecond precision.

        Usage:
            start_time = tracker.get_start_time()
            # Execute some function
            exec_time = tracker.get_exec_time("some_function", start_time)
            print(f"Execution time: {exec_time:.6f} seconds")
        """
        end_time = time.perf_counter()  # Use perf_counter for high-precision timing
        exec_time = end_time - start_time

        # Log the execution time with microsecond precision
        logger.debug(f"[{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(start_time))}] "
                     f"{func_name} took {exec_time:.6f} seconds to execute")

        # Store the execution time
        self._store_time(func_name, exec_time)
        return exec_time

    def _store_time(self, func_name: str, exec_time: float) -> None:
        """
        Store the execution time in the dictionary of tracked times, ensuring the max_count limit is respected.

        If the number of stored times exceeds max_count, the oldest time entry will be removed.

        Args:
            func_name (str): The name of the function whose execution time is being stored.
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
        Log the total and average execution times for all tracked functions.

        This method provides a summary of execution times for all functions that have been tracked,
        including the total and average times. It is useful for getting an overview of the performance
        of multiple functions that have been measured.

        Args:
            title (str): The title of the log summary. The default value is "Execution".
                         You can pass a custom title to differentiate between different reports.

        Usage:
            tracker.log_all_times()
            tracker.log_all_times(title="Custom Execution Summary")
        """
        # Log the start of the summary with the provided title
        logger.debug(f"~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ {title} --> Summary ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

        # Iterate over all tracked functions and their execution times
        for func_name, exec_times in self.times.items():
            total_time = sum(exec_times)  # Calculate the total execution time for the function
            avg_time = total_time / len(exec_times)  # Calculate the average execution time

            # Log the total and average execution times for each function
            logger.debug(
                f"Function: {func_name: <20} \t| Total Time: {total_time:.6f}s \t| Average Time: {avg_time:.6f}s"
            )

        # Log the end of the summary
        logger.debug("===============================================================================================")

    def log_single_time(self, label_name: str) -> None:
        """
        Log the total and average execution time for a specific function.

        Args:
            label_name (str): The name of the function whose execution times are to be logged.

        Usage:
            tracker.log_single_time("some_function")
            # Logs the total and average execution time for 'some_function'
        """
        if label_name in self.times:
            exec_times = self.times[label_name]
            total_time = sum(exec_times)
            avg_time = total_time / len(exec_times)
            logger.debug(
                f"Function: {label_name: <20} \t| Total Time: {total_time:.6f}s \t| Average Time: {avg_time:.6f}s")
        else:
            logger.warning(f"No data found for function: {label_name}")

    def get_total_time(self, label_name: str, log_time: bool = True) -> float:
        """
        Retrieve the total execution time for a specific function with detailed logging options.

        Args:
            label_name (str): The name of the function whose execution times are to be retrieved.
            log_time (bool): Whether to log the start time with detailed precision (default is True).

        Returns:
            float: The total execution time for the function. Returns 0 if no data is found.

        Usage:
            tracker.get_total_time("some_function", log_time=True)
            total_time = tracker.get_total_time("some_function", log_time=False)
        """
        if label_name in self.times:
            exec_times = self.times[label_name]
            total_time = sum(exec_times)  # 计算总时间

            if log_time:
                # Log the timestamp with year, month, day, hour, minute, second, millisecond, and microsecond
                start_time = time.perf_counter()  # High-precision timer
                local_time = time.localtime(start_time)
                formatted_time = time.strftime('%Y-%m-%d %H:%M:%S', local_time) + \
                                 f".{int((start_time % 1) * 1_000_000):06d}"

                # Log the total time along with the timestamp
                logger.debug(f"Total time for '{label_name}': {total_time:.6f} seconds "
                             f"({formatted_time})")

            return total_time
        else:
            logger.warning(f"No data found for function: {label_name}")
            return 0.0  # 如果没有找到数据，返回 0

    @contextmanager
    def time_code_block(self, label: str):
        """
        Context manager to track the execution time of code blocks.

        Args:
            label (str): The label to associate with the code block.

        Usage:
            with tracker.time_code_block("block_name"):
                # Code block
        """
        start_time = self.get_start_time()
        try:
            yield
        finally:
            exec_time = self.get_exec_time(label, start_time)
