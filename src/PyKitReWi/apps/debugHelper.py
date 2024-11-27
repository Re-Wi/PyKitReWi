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
    - v0.0.1 (2024/11/27 14:03)  重构接口，丰富功能
"""
from contextlib import contextmanager
import time
import asyncio
from typing import Callable, Any, Dict, List, Optional, Tuple
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

    def __init__(self, max_count: int = 33) -> None:
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

    def TrackTime(self, func: Callable) -> Callable:
        """
        A decorator that tracks the execution time of a function (either synchronous or asynchronous).

        This decorator wraps the given function and records its execution time. It works with both
        synchronous and asynchronous functions.

        Args:
            func (Callable): The function whose execution time will be tracked.

        Returns:
            Callable: The wrapped function with time-tracking functionality.

        Usage:
            @tracker.TrackTime
            def some_function():
                # Function code to be executed
        """

        @wraps(func)
        async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
            """Wrapper for asynchronous functions."""
            start_time = self.GetStartTime(log_time=False)

            # Execute the original function asynchronously
            result = await func(*args, **kwargs)

            exec_time = self._GetExecTime(start_time, label_name=func.__name__)
            return result

        @wraps(func)
        def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
            """Wrapper for synchronous functions."""
            start_time = self.GetStartTime(log_time=False)

            # Execute the original function
            result = func(*args, **kwargs)

            exec_time = self._GetExecTime(start_time, label_name=func.__name__)
            return result

        # Return async wrapper if the function is asynchronous, otherwise return sync wrapper
        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        else:
            return sync_wrapper

    def GetStartTime(self, log_time: bool = True) -> float:
        """
        Get the current time in seconds since the epoch with high precision, which will be used to calculate execution time.

        Optionally, logs the start time with microsecond precision if log_time is True.

        Args:
            log_time (bool): A flag to determine whether to log the start time.
                             If True, logs the start time with microsecond precision.
                             If False, does not log the start time.

        Returns:
            float: The start time in seconds with microsecond precision.

        Usage:
            # Example 1: Get start time and log it
            start_time = tracker.GetStartTime(log_time=True)  # Logs the start time

            # Example 2: Get start time without logging
            start_time = tracker.GetStartTime(log_time=False)  # Does not log the start time
        """
        # Get high-precision start time
        start_time = time.perf_counter()

        # Log the start time if log_time is True
        if log_time:
            # Convert start time to local time (in seconds)
            local_time = time.localtime(time.time())  # Use time.time() for real-world time
            formatted_time = time.strftime('%Y-%m-%d %H:%M:%S',
                                           local_time) + f".{int((time.time() % 1) * 1_000_000):06d}"

            # Log the formatted start time with Epoch time
            logger.debug(f"Start time: {formatted_time} (Epoch time: {start_time:.6f} seconds)")

        return start_time

    def _GetExecTime(self, start_time: float, label_name: str = "default_label") -> float:
        """
        Calculate and log the execution time of a function with microsecond precision.

        Args:
            start_time (float): The timestamp when the function started executing.
            label_name (str): The name of the code whose execution time is being tracked.
                              Defaults to "default_label" if not provided.

        Returns:
            float: The execution time in seconds, including microsecond precision.

        Usage:
            start_time = tracker.GetStartTime()
            # Execute some function
            elapsed_time = tracker._GetExecTime(start_time)
            print(f"Execution time: {elapsed_time:.6f} seconds")

            # With custom label and no logging
            elapsed_time = tracker._GetExecTime(start_time, "custom_label")
        """
        # Get the end time using high-precision timer
        end_time = time.perf_counter()

        # Calculate elapsed time in seconds
        elapsed_time = end_time - start_time

        # Store the execution time
        self._StoreTime(label_name, elapsed_time)

        # Return the elapsed time for further use
        return elapsed_time

    def GetExecTimeDetails(self, start_time: float, label_name: str = "default_label", log_time: bool = True) -> Dict:
        """
        Calculate and log the execution time of a process with microsecond precision.

        Args:
            start_time (float): The timestamp when the process started executing.
            label_name (str): The label associated with the process whose execution time is being tracked.
                              Defaults to "default_label" if not provided.
            log_time (bool): Whether to log the execution time. Default is True.
                             If False, the execution time will not be logged.

        Returns:
            Dict: A dictionary containing the calculated execution time, including:
                - "days" (int): The number of days.
                - "hours" (int): The number of hours.
                - "minutes" (int): The number of minutes.
                - "seconds" (int): The number of seconds.
                - "milliseconds" (int): The number of milliseconds.
                - "microseconds" (int): The number of microseconds.
                - "total_seconds" (float): The total execution time in seconds.

        Usage:
            start_time = tracker.GetStartTime()
            # Execute some function
            execution_times = tracker.GetExecTimeDetails(start_time)  # Logs time with default label
            execution_times = tracker.GetExecTimeDetails(start_time, "custom_label")  # Logs time with custom label
        """
        elapsed_time = self._GetExecTime(start_time, label_name=label_name)

        # Convert elapsed time to days, hours, minutes, seconds, milliseconds, and microseconds
        days, remainder = divmod(elapsed_time, 86400)  # 86400 seconds in a day
        hours, remainder = divmod(remainder, 3600)  # 3600 seconds in an hour
        minutes, remainder = divmod(remainder, 60)  # 60 seconds in a minute
        seconds, remainder = divmod(remainder, 1)  # Whole seconds
        milliseconds, microseconds = divmod(remainder * 1_000, 1_000)  # Milliseconds and microseconds

        # Log the execution time with microseconds, avoiding 1970 issue
        if log_time:
            current_time = time.time()  # Get current time in seconds since epoch
            local_time = time.localtime(current_time)
            formatted_time = time.strftime('%Y-%m-%d %H:%M:%S',
                                           local_time) + f".{int((current_time % 1) * 1_000_000):06d}"

            logger.debug(f"[{formatted_time}] {label_name} took {int(days)} days {int(hours)} hours "
                         f"{int(minutes)} minutes {int(seconds)} seconds {int(milliseconds)} milliseconds "
                         f"{int(microseconds)} microseconds")

        # Return the execution time as a dictionary
        return {
            "days": days,
            "hours": hours,
            "minutes": minutes,
            "seconds": seconds,
            "milliseconds": milliseconds,
            "microseconds": microseconds,
            "total_seconds": elapsed_time
        }

    def _StoreTime(self, label_name: str, exec_time: float) -> None:
        """
        Store the execution time in the dictionary of tracked times, ensuring the max_count limit is respected.

        If the number of stored times exceeds max_count, the oldest time entry will be removed.

        Args:
            label_name (str): The name of the function or code whose execution time is being stored.
            exec_time (float): The execution time in seconds.
        """
        if label_name not in self.times:
            self.times[label_name] = []
        self.times[label_name].append(exec_time)
        if len(self.times[label_name]) > self.max_count:
            # Remove the oldest execution time if the limit is exceeded
            self.times[label_name].pop(0)

    @contextmanager
    def TimeCodeBlock(self, label: str) -> None:
        """
        Context manager to track the execution time of code blocks.

        Args:
            label (str): The label to associate with the code block.

        Usage:
            with tracker.TimeCodeBlock("example_block"):
                # Code to track
        """
        start_time = self.GetStartTime(log_time=False)
        try:
            yield
        finally:
            exec_time = self._GetExecTime(start_time, label_name=label)

    def LogTimeReport(self, title="Execution") -> None:
        """
        Log the total and average execution times for all tracked functions.

        This method provides a summary of execution times for all functions that have been tracked,
        including the total and average times. It is useful for getting an overview of the performance
        of multiple functions that have been measured.

        Args:
            title (str): The title of the log summary. The default value is "Execution".
                         You can pass a custom title to differentiate between different reports.

        Usage:
            tracker.LogTimeReport()
            tracker.LogTimeReport(title="Custom Execution Summary")
        """
        # Check if there are any recorded times
        if not self.times:
            logger.debug("No execution times to report.")
            return
        # Log the start of the summary with the provided title
        logger.debug(f"~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ {title} --> Summary ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

        # Iterate over all tracked functions and their execution times
        logger.debug(f"           label_name            \t |  Average Time (s)  \t |   Total Time (s) \t | times ")
        for label_name, exec_times in self.times.items():
            total_time = sum(exec_times)  # Calculate the total execution time for the function
            times = len(exec_times)
            avg_time = total_time / times if exec_times else 0  # Calculate the average execution time

            # Log the total and average execution times for each function
            logger.debug(f"{label_name: <33} \t | {avg_time:.6f}s \t | {total_time:.6f}s \t | {times}")

        # Log the end of the summary
        logger.debug("===============================================================================================")

    def GetSingleLabelTime(self, label_name: str, log_time: Optional[bool] = True) -> Tuple[float, float]:
        """
        Logs the total and average execution time for a specific function, with optional high-precision timestamp logging.
        Returns the total and average execution times, or (0.0, 0.0) if the label is not found.

        Args:
            label_name (str): The name of the function whose execution times are to be logged.
            log_time (Optional[bool]): Whether to log the detailed timestamp with high precision (default is True).

        Returns:
            Tuple[float, float]: A tuple containing the total and average execution times for the specified function.
                                 If the function is not found, returns (0.0, 0.0).

        Usage:
            total_time, avg_time = tracker.GetSingleLabelTime("label_name", log_time=True)
            # Logs the total, average execution time, and timestamp for 'label_name'
        """
        if label_name in self.times:
            exec_times = self.times[label_name]
            total_time = sum(exec_times)
            times = len(exec_times)
            avg_time = total_time / times if exec_times else 0

            # Log total and average execution times
            logger.debug(
                f"label_name: {label_name: <20} \t | Average Time: {avg_time:.6f}s \t | Total Time: {total_time:.6f}s \t | {times} ")

            if log_time:
                # Log the timestamp with year, month, day, hour, minute, second, millisecond, and microsecond
                start_time = time.perf_counter()  # High-precision timer
                local_time = time.localtime(start_time)
                formatted_time = time.strftime('%Y-%m-%d %H:%M:%S', local_time) + \
                                 f".{int((start_time % 1) * 1_000_000):06d}"

                # Log the timestamp
                logger.debug(f"Timestamp for '{label_name}': {formatted_time}")

            # Return total time and average time
            return total_time, avg_time

        else:
            logger.warning(f"No data found for label_name: {label_name}")
            # Return default values if no data is found
            return 0.0, 0.0
