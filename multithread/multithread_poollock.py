from concurrent.futures import ThreadPoolExecutor
from threading import current_thread
from threading import Lock
import os
import time

a = 1


lock = Lock()  # 实例化一个锁


def task(url):
    lock.acquire()  # 加锁

    global a
    time.sleep(1)  # 模拟耗时操作
    print(f"线程名: {current_thread().name}, 进程号: {os.getpid()}, a: {a}, url: {url}")
    a += 1

    lock.release()  # 解锁


executor = ThreadPoolExecutor(max_workers=3)  # 创建一个线程池，最多同时执行3个线程
for i in range(1, 11):
    executor.submit(task, i)  # 提交任务到线程池
executor.shutdown()  # 关闭线程池，不再接受新的线程

"""
>>>
线程名: ThreadPoolExecutor-0_0, 进程号: 3824, a: 1, url: 1
线程名: ThreadPoolExecutor-0_1, 进程号: 3824, a: 2, url: 2
线程名: ThreadPoolExecutor-0_2, 进程号: 3824, a: 3, url: 3
线程名: ThreadPoolExecutor-0_0, 进程号: 3824, a: 4, url: 4
线程名: ThreadPoolExecutor-0_1, 进程号: 3824, a: 5, url: 5
线程名: ThreadPoolExecutor-0_2, 进程号: 3824, a: 6, url: 6
线程名: ThreadPoolExecutor-0_0, 进程号: 3824, a: 7, url: 7
线程名: ThreadPoolExecutor-0_1, 进程号: 3824, a: 8, url: 8
线程名: ThreadPoolExecutor-0_2, 进程号: 3824, a: 9, url: 9
线程名: ThreadPoolExecutor-0_0, 进程号: 3824, a: 10, url: 10
"""

"""
第5、7、12行代码就是对线程池代码的任务函数做了加锁和解锁操作，主要是确保同一时间只有一个线程在使用共享资源。
加锁会让代码执行效率变低，但是不用担心，因为在实际的爬虫程序中应用线程池时一般会使用队列，而队列会自己做加锁和解锁的操作，以保证队列中的一个任务只会被一个线程执行，并且有多个任务等待被执行，不会造成多个线程等待一个任务的情况。
如果为了保证数据安全不得不使用全局变量，则必须加锁，造成的执行效率变低是不可避免的。虽然效率变低了，但是相较于使用同一个线程来处理爬虫任务，速度还是快了很多。
"""
