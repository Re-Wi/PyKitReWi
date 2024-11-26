# -*- coding: UTF-8 -*-
"""
@Project    : PyKitReWi
@File       : logsRecorder.py
@IDE        : PyCharm
@Author     : ReWi  # 替换为当前系统用户名（方便开发人员区分）
@Date       : 2024/11/26 17:03  # 日期和时间精确到秒
@License    : MIT
@Contact    : RejoiceWindow <RejoiceWindow@yeah.net>
@Description: 日志记录器
@Version    : v0.0.0
@Dependencies: 
    - python3
@Changelog  : 
    - v0.0.0 (2024/11/26 17:03): Initial version, implemented the core functionality.
    - v0.0.1 (2024/11/26 17:03)  # 记录文件版本更新的日志，例如修复的bug、增加的功能等
"""
import os
import sys
import datetime
from loguru import logger
from typing import Optional

from ..utils.filePathHelper import NoDuplicateFile, EnsureFolders


class LogsRecorder:
    """
    A class that handles the initialization and management of log files. It allows logging with rotation,
    retention, and compression options. The log file name includes the script name and a timestamp to ensure
    uniqueness and prevent overwriting.

    Attributes:
        directory (str): The directory where log files will be stored. Defaults to './data/logs/'.
        log_filename (str): The name of the log file. Defaults to the script name with timestamp.
        log_filepath (str): The full file path of the log file, including the directory and file name.
        logger_id (int): The unique identifier for the logger instance, used for further management.

    Methods:
        __init__(log_dir: str, log_name: Optional[str]): Initializes the logger with the specified directory and filename.
        ensure_directory_exists(directory: str): Ensures the log directory exists. If not, it will create it.
        no_duplicate_file(directory: str, filename: str, extension: str): Ensures the log file does not already exist.
        init_logger(): Initializes the logger and sets up log rotation, retention, and compression.
        get_logger(): Returns the logger instance for logging messages.
    """

    def __init__(self, log_dir: str = './data/logs/', log_name: Optional[str] = None) -> None:
        """
        Initializes the logger with a specified log directory and log file name.

        Args:
            log_dir (str): The directory where the log file will be saved. Defaults to './data/logs/'.
            log_name (Optional[str]): The name of the log file. If not provided, the log file name is generated using
                                      the script name and current timestamp.
        """
        # Set default log directory and file name if not provided
        self.directory: str = log_dir
        self.log_filename: str = log_name or os.path.basename(sys.argv[0]).split(".")[
            0] + "--" + datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S-%f')
        self.log_filepath: str = os.path.join(self.directory, self.log_filename)

        # Ensure the log directory exists
        log_dir = EnsureFolders(self.directory)

        # Check for duplicates in log file names
        self.log_filepath = NoDuplicateFile(self.directory, self.log_filename, file_extension='.log')

        # Initialize the logger
        self.logger_id: int = self.init_logger()

    def init_logger(self) -> int:
        """
        Initializes the logger with rotation, retention, and compression settings.

        The log file is created with the specified path. The logger will rotate the log file when it reaches
        10MB in size, and will retain logs for up to 60 days. Older logs are compressed into zip files.

        Returns:
            int: The unique logger ID used to reference this logger instance for future management.

        Usage:
            logger_id = log_recorder.init_logger()  # Initializes the logger and sets up configurations.
        """
        # Remove any existing default logger, the console will not appear, just save to file
        # logger.remove()

        # Add a new logger with rotation, retention, and compression
        log_id: int = logger.add(self.log_filepath,
                                 rotation="10 MB",  # Rotate the log file after it reaches 10MB
                                 retention="60 days",  # Keep logs for 60 days
                                 compression="zip",  # Compress rotated logs as zip files
                                 enqueue=True)  # Enable async logging

        # Print the path of the log file for user reference
        print(f'Logger initialized. Logs will be saved to: {self.log_filepath}')
        return log_id

    def get_logger(self) -> logger:
        """
        Returns the logger instance for logging messages.

        Returns:
            logger: The logger instance, which can be used for logging at different levels (info, debug, etc.).

        Usage:
            logger = log_recorder.get_logger()
            logger.info("This is an informational message.")
        """
        return logger
