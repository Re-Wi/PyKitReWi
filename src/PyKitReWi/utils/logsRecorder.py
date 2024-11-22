import os
import sys
from loguru import logger
import datetime
from .filePathHelper import EnsureFolders, NoDuplicateFile


class LogsRecorder:
    directory = './data/logs/'
    # log_name = sys.argv[0].split(".")[0].split("/")[-1] + ".log" # 获取运行脚本名
    log_filename = os.path.basename(sys.argv[0]).split(".")[0] + "--" + datetime.datetime.now().strftime(
        '%Y-%m-%d_%H-%M-%S-%f')
    log_filepath = directory + log_filename

    def InitLogger(self, log_dir=directory, log_name=log_filename):
        if len(log_dir) > 1:
            self.directory = EnsureFolders(log_dir)
        if len(log_name) > 1:
            self.log_filename = log_name
        self.log_filepath = NoDuplicateFile(self.directory, self.log_filename, '.log')
        print('logger :', self.log_filepath)
        id = log = logger.add(self.log_filepath, rotation="10 MB", retention="60 days", compression="zip", enqueue=True)

    # def b_function1(x):
    #     try:
    #         return 1 / x
    #     except ZeroDivisionError:
    #         logger.exception("exception!!!")
    #
    # b_function1(0)
    # logger.remove(id)
# logRecorder =LogRecorder()
# logRecorder.InitLogger()
# logger.debug('this is a debug message')
# logger.debug('i am debug message')
# logger.info('i am info message')
# logger.error('i am error message')
# logger.success('i am success message')
