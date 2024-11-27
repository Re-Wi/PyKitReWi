import time
import asyncio
import unittest
from unittest.mock import patch

from src.PyKitReWi.apps.debugHelper import TimeTracker


class TestTimeTracker(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        # Create a fresh TimeTracker instance before each test
        self.tracker = TimeTracker(max_count=3)

    # Test 1: Test the TrackTime decorator on a synchronous function with strict timing
    def test_sync_function_tracking(self):
        @self.tracker.TrackTime
        def slow_function():
            time.sleep(0.1)  # Simulating some processing time

        start_time = time.perf_counter()  # Start time before calling the function
        slow_function()  # Run the function once
        end_time = time.perf_counter()  # End time after function execution

        total_time, avg_time = self.tracker.GetSingleLabelTime("slow_function")

        # Ensure the execution time is within a reasonable range (e.g., 0.1s ± 0.02s)
        self.assertGreater(total_time, 0.08)
        self.assertLess(total_time, 0.12)

        # Ensure that the recorded time is close to the actual execution time
        self.assertGreater(avg_time, 0.08)
        self.assertLess(avg_time, 0.12)

    # Test 2: Test the TrackTime decorator on an asynchronous function with strict timing
    async def test_async_function_tracking(self):
        @self.tracker.TrackTime
        async def slow_async_function():
            await asyncio.sleep(0.1)  # Simulating async processing time

        start_time = time.perf_counter()  # Start time before calling the async function
        await slow_async_function()  # Run the async function
        end_time = time.perf_counter()  # End time after async function execution

        total_time, avg_time = self.tracker.GetSingleLabelTime("slow_async_function")

        # Ensure the execution time is within a reasonable range (e.g., 0.1s ± 0.02s)
        self.assertGreater(total_time, 0.08)
        self.assertLess(total_time, 0.12)

        # Ensure that the recorded time is close to the actual execution time
        self.assertGreater(avg_time, 0.08)
        self.assertLess(avg_time, 0.12)

    # Test 3: Test GetStartTime method with strict timing control
    def test_get_start_time(self):
        start_time = self.tracker.GetStartTime(log_time=False)
        self.assertIsInstance(start_time, float)
        time.sleep(0.1)
        end_time = self.tracker.GetStartTime(log_time=False)

        # Ensure that the difference between start and end time is at least 0.1 seconds
        self.assertGreater(end_time - start_time, 0.1)

    # Test 4: Test GetExecTimeDetails method with strict time checking
    def test_get_exec_time_details(self):
        start_time = self.tracker.GetStartTime(log_time=False)
        time.sleep(0.1)  # Simulate some processing time
        details = self.tracker.GetExecTimeDetails(start_time)

        self.assertIn("total_seconds", details)
        self.assertGreater(details["total_seconds"], 0.08)  # Ensure it took at least 0.08s
        self.assertLess(details["total_seconds"], 0.12)  # Ensure it didn’t take too long (e.g., more than 0.12s)

    # Test 5: Test TimeCodeBlock context manager with strict timing control
    def test_time_code_block(self):
        with self.tracker.TimeCodeBlock("code_block_test"):
            time.sleep(0.1)  # Simulate code block execution time

        total_time, avg_time = self.tracker.GetSingleLabelTime("code_block_test")

        # Ensure the execution time is within a reasonable range (e.g., 0.1s ± 0.02s)
        self.assertGreater(total_time, 0.08)
        self.assertLess(total_time, 0.12)

        # Ensure that the recorded time is close to the actual execution time
        self.assertGreater(avg_time, 0.08)
        self.assertLess(avg_time, 0.12)

    # Test 6: Test LogTimeReport method with timing constraints
    @patch("loguru.logger.debug")  # Mocking the logger to prevent actual logging output
    def test_log_time_report(self, mock_logger):
        self.tracker.LogTimeReport(title="Test Execution Report")
        mock_logger.assert_called()  # Ensure logger.debug was called

    # Test 7: Test GetSingleLabelTime method with a non-existent label
    def test_get_single_label_time_no_data(self):
        total_time, avg_time = self.tracker.GetSingleLabelTime("non_existent_label")
        self.assertEqual(total_time, 0.0)
        self.assertEqual(avg_time, 0.0)

    # Test 8: Test LogTimeReport when no times are recorded
    @patch("loguru.logger.debug")
    def test_log_time_report_no_times(self, mock_logger):
        empty_tracker = TimeTracker(max_count=3)  # Create a new instance with no times recorded
        empty_tracker.LogTimeReport(title="Empty Report")
        mock_logger.assert_called_with("No execution times to report.")


# Run the tests
if __name__ == "__main__":
    unittest.main()
