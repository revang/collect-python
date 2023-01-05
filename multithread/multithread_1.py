from threading import Thread
import time

"""
一个进程中能存在多个线程，一个线程遇到I/O阻塞时会处于挂起状态，此时其他线程会来争抢CPU资源，CPU就会去执行其他线程。
线程的切换速度很快，快到能使人发现不了两个任务的执行其实是有先后顺序的，感觉所有线程是在同时运行一样，这就是并发的效果。
而且线程占用系统资源小，执行速度更快，所以使用多线程可以提高程序的运行效率。Python的threading模块提供了创建线程的方法。
"""


def task(url):
    print("开始执行: ", url)
    time.sleep(2)
    print("结束执行: ", url)


if __name__ == '__main__':
    print("main start")
    t1 = Thread(target=task, args=("http://www.baidu.com",))
    t2 = Thread(target=task, args=("http://www.google.com",))
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    print("main end")

"""
>>>
main start
开始执行:  http://www.baidu.com
开始执行:  http://www.google.com
结束执行:  http://www.baidu.com
结束执行:  http://www.google.com
main end
"""
