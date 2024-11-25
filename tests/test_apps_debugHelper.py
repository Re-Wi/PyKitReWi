import time
import asyncio
import unittest
from src.PyKitReWi.apps.debugHelper import TimeTracker


class TestTimeTracker(unittest.TestCase):

    def test_同步函数跟踪(self):
        """
        测试同步函数的执行时间跟踪
        """
        tracker = TimeTracker()

        @tracker.track_time
        def sample_sync_function():
            time.sleep(1)  # 模拟一个耗时操作

        # 调用函数
        sample_sync_function()
        sample_sync_function()

        # 查看所有函数的执行时间汇总并断言
        tracker.log_all_times()
        # 可以根据实际的时间范围设置期望的时间值，例如 0.9 到 1.1 秒之间
        self.assertGreaterEqual(tracker.get_total_time("sample_sync_function"), 2.0)
        self.assertLessEqual(tracker.get_total_time("sample_sync_function"), 2.2)

    def test_异步函数跟踪(self):
        """
        测试异步函数的执行时间跟踪
        """
        tracker = TimeTracker()

        async def sample_async_function():
            await asyncio.sleep(1)
            print("Async function executed!")

        # 使用 track_time 装饰器装饰异步函数
        @tracker.track_time
        async def decorated_async_function():
            await sample_async_function()

        # 获取当前事件循环
        loop = asyncio.get_event_loop()

        # 如果事件循环已经在运行，使用 create_task
        if loop.is_running():
            task = loop.create_task(decorated_async_function())
            task.add_done_callback(lambda t: tracker.log_all_times())  # 任务完成后查看执行时间
        else:
            # 如果没有事件循环，使用 asyncio.run 运行
            asyncio.run(decorated_async_function())

        # 查看指定函数的执行时间记录
        tracker.log_single_time("decorated_async_function")
        self.assertGreaterEqual(tracker.get_total_time("decorated_async_function"), 1.0)
        self.assertLessEqual(tracker.get_total_time("decorated_async_function"), 1.2)

    def test_代码片段进行计时(self):
        """
        测试代码片段的计时功能
        """
        tracker = TimeTracker()

        # 开始计时
        start_time = tracker.get_start_time()

        # 要计时的代码片段
        time.sleep(1)  # 模拟耗时操作

        # 记录执行时间
        tracker.get_exec_time("代码片段进行计时", start_time)

        # 查看执行时间汇总并断言
        tracker.log_all_times()
        self.assertGreaterEqual(tracker.get_total_time("代码片段进行计时"), 1.0)
        self.assertLessEqual(tracker.get_total_time("代码片段进行计时"), 1.2)

    def test_灵活的代码片段计时(self):
        """
        测试灵活的代码片段计时功能
        """
        tracker = TimeTracker()

        # 计时一个代码块
        with tracker.time_code_block("灵活的代码片段计时"):
            time.sleep(1)  # 模拟耗时操作

        # 查看执行时间汇总并断言
        tracker.log_all_times()
        self.assertGreaterEqual(tracker.get_total_time("灵活的代码片段计时"), 1.0)
        self.assertLessEqual(tracker.get_total_time("灵活的代码片段计时"), 1.2)


if __name__ == '__main__':
    unittest.main()