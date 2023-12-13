# -*- coding: utf-8 -*-
# Author : Ethan
# Time : 2023/12/11 11:04
import time

def pytest_configure(config):  # noqa
    config.addinivalue_line(
        "markers", "timeassert: run timeout"
    )

def pytest_runtest_call(item):
    timeout = item.keywords.get('timeassert', None)
    if timeout:
        time_value = timeout.args[0]
        start_time = time.time()
        item.runtest()  # 执行测试用例
        end_time = time.time()
        assert end_time - start_time < float(time_value), "Test execution time exceeded the threshold"
    else:
        item.runtest()

