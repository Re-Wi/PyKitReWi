import time
import unittest
from src.PyKitReWi.utils.timeUtils import DelaySeconds, DelayMilliseconds, DelayMicroseconds, DelayNanoseconds


class TestHighPrecisionDelay(unittest.TestCase):

    # 测试延时秒数
    def test_DelaySeconds(self):
        start_time = time.perf_counter()
        DelaySeconds(1)  # 延时 1 秒
        end_time = time.perf_counter()
        elapsed_time = end_time - start_time
        self.assertGreaterEqual(elapsed_time, 1.0, f"Expected delay of 1 second, but got {elapsed_time} seconds.")
        self.assertLess(elapsed_time, 1.01, f"Expected delay of 1 second, but got {elapsed_time} seconds.")

    # 测试延时毫秒数
    def test_DelayMilliseconds(self):
        start_time = time.perf_counter()
        DelayMilliseconds(500)  # 延时 500 毫秒
        end_time = time.perf_counter()
        elapsed_time = end_time - start_time
        self.assertGreaterEqual(elapsed_time * 1000, 499,
                                f"Expected delay of 500 milliseconds, but got {elapsed_time * 1000} milliseconds.")
        self.assertLess(elapsed_time * 1000, 501,
                        f"Expected delay of 500 milliseconds, but got {elapsed_time * 1000} milliseconds.")

    # 测试延时微秒数
    def test_DelayMicroseconds(self):
        start_time = time.perf_counter()
        DelayMicroseconds(1000000)  # 延时 1000000 微秒 (即 1 秒)
        end_time = time.perf_counter()
        elapsed_time = end_time - start_time
        self.assertGreaterEqual(elapsed_time, 1.0, f"Expected delay of 1 second, but got {elapsed_time} seconds.")
        self.assertLess(elapsed_time, 1.01, f"Expected delay of 1 second, but got {elapsed_time} seconds.")

    # 测试延时纳秒数
    def test_DelayNanoseconds(self):
        start_time = time.perf_counter()
        DelayNanoseconds(1000000000)  # 延时 1000000000 纳秒 (即 1 秒)
        end_time = time.perf_counter()
        elapsed_time = end_time - start_time
        self.assertGreaterEqual(elapsed_time, 1.0, f"Expected delay of 1 second, but got {elapsed_time} seconds.")
        self.assertLess(elapsed_time, 1.01, f"Expected delay of 1 second, but got {elapsed_time} seconds.")

    # 测试极小的延时（微秒级）
    def test_DelayMicroseconds_small(self):
        start_time = time.perf_counter()
        DelayMicroseconds(1)  # 延时 1 微秒
        end_time = time.perf_counter()
        elapsed_time = end_time - start_time
        self.assertLess(elapsed_time * 1000000, 1,
                        f"Expected delay less than 1 millisecond, but got {elapsed_time * 1000} milliseconds.")

    # 测试极小的延时（纳秒级）
    def test_DelayNanoseconds_small(self):
        start_time = time.perf_counter()
        DelayNanoseconds(100)  # 延时 100 纳秒
        end_time = time.perf_counter()
        elapsed_time = end_time - start_time
        self.assertLess(elapsed_time * 1000000000, 1,
                        f"Expected delay less than 1 microsecond, but got {elapsed_time * 1000000} microseconds.")


if __name__ == '__main__':
    unittest.main()
