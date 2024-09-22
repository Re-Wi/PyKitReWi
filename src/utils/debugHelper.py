import time
from loguru import logger
from typing import Callable, Any, List, Dict


class TimeTracker:
    def __init__(self):
        """
        Initialize a TimeTracker instance that stores execution times for multiple functions.
        Attributes:
            times (dict): A dictionary where keys are function names (str) and values are lists of execution times (float).
        """
        self.times: Dict[str, List[float]] = {}

    def track_time(self, func: Callable) -> Callable:
        """
        Decorator function that wraps a given function and tracks its execution time.

        Args:
            func (Callable): The function whose execution time is to be tracked.

        Returns:
            Callable: The wrapped function with time-tracking functionality.
        """

        def wrapper(*args: Any, **kwargs: Any) -> Any:
            # Record start time
            start_time = time.time()

            # Execute the original function and get its result
            result = func(*args, **kwargs)

            # Record end time
            end_time = time.time()

            # Calculate the time it took to execute the function
            exec_time = end_time - start_time

            # Log the execution time using loguru
            logger.info(f"{func.__name__} took {exec_time:.6f} seconds to execute")

            # Store the execution time in the times dictionary
            if func.__name__ in self.times:
                self.times[func.__name__].append(exec_time)
            else:
                self.times[func.__name__] = [exec_time]

            # Return the original result of the function
            return result

        return wrapper

    def log_all_times(self) -> None:
        """
        Logs the total and average execution times for all tracked functions.

        Output:
            Logs the execution time summary for all tracked functions using loguru.
        """
        logger.info("Execution Time Summary:")
        for func_name, exec_times in self.times.items():
            total_time = sum(exec_times)
            avg_time = total_time / len(exec_times)
            logger.info(f"Function: {func_name} | Total Time: {total_time:.6f}s | Average Time: {avg_time:.6f}s")

    def log_single_time(self, func_name: str) -> None:
        """
        Logs the total and average execution time for a specific function.

        Args:
            func_name (str): The name of the function whose execution times are to be logged.

        Output:
            Logs the total and average execution time for the specified function. If no data exists, logs a warning.
        """
        if func_name in self.times:
            exec_times = self.times[func_name]
            total_time = sum(exec_times)
            avg_time = total_time / len(exec_times)
            logger.info(f"Function: {func_name} | Total Time: {total_time:.6f}s | Average Time: {avg_time:.6f}s")
        else:
            logger.warning(f"No data found for function: {func_name}")
