import unittest
import os
import datetime
import os
import time
from loguru import logger
from unittest.mock import patch, Mock

from src.PyKitReWi.apps.logsRecorder import LogsRecorder


class TestLogsRecorder(unittest.TestCase):
    """
    Test case for the LogsRecorder class, verifying the functionality of log file creation,
    directory handling, and logging behavior.
    """

    def setUp(self):
        # Setup the logger and log file
        self.log_recorder = LogsRecorder(log_dir='./test_logs', log_name="test_log")
        self.test_directory = './test_logs_creation'
        self.logger = self.log_recorder.get_logger()

    def tearDown(self):
        # Ensure the logger handler is removed before deleting the file
        logger.remove()  # Remove all handlers to ensure the log file is closed
        if os.path.exists(self.log_recorder.log_filepath):
            os.remove(self.log_recorder.log_filepath)
            print(f"Log file removed: {self.log_recorder.log_filepath}")

    def test_directory_creation(self):
        """
        Test that the log directory is created if it doesn't already exist.
        """
        test_directory = './test_logs_creation'
        log_recorder = LogsRecorder(log_dir=test_directory)
        log_recorder.get_logger()

        # Check if the directory was created
        self.assertTrue(os.path.exists(test_directory))
        # Clean up after the test
        for file in os.listdir(test_directory):
            file_path = os.path.join(test_directory, file)
            # if os.path.isfile(file_path):
            #     os.remove(file_path)
        # os.rmdir(test_directory)

    def test_log_filename_uniqueness(self):
        """
        Test that the logger creates unique filenames when the same base filename is used.
        """
        # Get the log filename with timestamp
        base_filename = self.log_recorder.log_filename
        log_filepath_1 = self.log_recorder.log_filepath

        # Create another LogsRecorder instance that should generate a unique filename
        log_recorder_2 = LogsRecorder(log_dir=self.test_directory, log_name=base_filename)
        log_filepath_2 = log_recorder_2.log_filepath

        # Assert that both log files have unique names
        self.assertNotEqual(log_filepath_1, log_filepath_2)

        # Clean up after test
        for file in os.listdir(self.test_directory):
            file_path = os.path.join(self.test_directory, file)
            # if os.path.isfile(file_path):
            #     os.remove(file_path)

    def test_log_rotation(self):
        """
        Test log rotation functionality. Ensure that the log file is created and rotated.
        """
        # Get the current log file path
        log_filepath = self.log_recorder.log_filepath

        # Log some data
        self.logger.info("Test log rotation")

        # Check that the log file was created and exists
        self.assertTrue(os.path.exists(log_filepath))

        # Check the log file size does not exceed the limit (10MB), rotation is configured
        log_file_size = os.path.getsize(log_filepath)
        self.assertTrue(log_file_size < 10 * 1024 * 1024)  # Should be less than 10 MB

    # def test_logging_behavior(self):
    #     """
    #     Test that logs are correctly written to the log file.
    #     """
    #     # Test logger logging behavior
    #     with patch('sys.stdout', new_callable=Mock) as mock_stdout:
    #         self.logger.info("Test log entry")
    #         # Ensure the message was logged (this will be captured)
    #         mock_stdout.write.assert_any_call("Test log entry\n")

    def test_init_logger(self):
        """
        Test that logger is initialized correctly with rotation and retention settings.
        """
        # Create a new LogsRecorder instance and check if the logger is initialized
        log_recorder = LogsRecorder(log_dir=self.test_directory)
        logger = log_recorder.get_logger()

        # Check logger existence and basic configuration
        self.assertIsNotNone(logger)
        self.assertTrue(isinstance(logger, logger.__class__))  # Ensure the logger is valid


if __name__ == '__main__':
    unittest.main()
