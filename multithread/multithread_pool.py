from concurrent.futures import ThreadPoolExecutor
from threading import current_thread
import os
import time

a = 1


def task(url):
    global a
    time.sleep(1)  # 模拟耗时操作
    print(f"线程名: {current_thread().name}, 进程号: {os.getpid()}, a: {a}, url: {url}")
    a += 1


executor = ThreadPoolExecutor(max_workers=3)  # 创建一个线程池，最多同时执行3个线程
for i in range(1, 11):
    executor.submit(task, i)  # 提交任务到线程池
executor.shutdown()  # 关闭线程池，不再接受新的线程

"""
>>>
线程名: ThreadPoolExecutor-0_1, 进程号: 22660, a: 1, url: 2
线程名: ThreadPoolExecutor-0_0, 进程号: 22660, a: 1, url: 1
线程名: ThreadPoolExecutor-0_2, 进程号: 22660, a: 1, url: 3
线程名: ThreadPoolExecutor-0_1, 进程号: 22660, a: 4, url: 4
线程名: ThreadPoolExecutor-0_0, 进程号: 22660, a: 4, url: 5
线程名: ThreadPoolExecutor-0_2, 进程号: 22660, a: 4, url: 6
线程名: ThreadPoolExecutor-0_0, 进程号: 22660, a: 7, url: 8
线程名: ThreadPoolExecutor-0_1, 进程号: 22660, a: 7, url: 7
线程名: ThreadPoolExecutor-0_2, 进程号: 22660, a: 7, url: 9
线程名: ThreadPoolExecutor-0_0, 进程号: 22660, a: 10, url: 10
"""

"""
细心的读者可能会发现相同的线程处理了不同的任务，其实本质上并非如此，只是在同一时刻有多个线程在运行，线程之间可以直接通信，所以它们能同时读取全局变量a，就会得到相同的值。
这是线程共享全局变量带来的数据安全隐患，可以通过加锁来解决：使用Lock类实例化一个锁，在调用共享全局变量的前后分别进行加锁和解锁的操作。
"""
