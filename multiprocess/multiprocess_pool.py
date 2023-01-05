import os
import time
from multiprocessing import Process
from multiprocessing.pool import Pool


def task(i):
    print('子进程开始执行：', i)
    time.sleep(2)
    print('子进程执行结束：', i)


if __name__ == '__main__':
    print('父进程开始执行')
    p = Pool(4)  # 创建一个进程池，最多同时执行4个进程
    for i in range(1, 11):
        p.apply_async(task, args=(i,))  # 异步执行进程，不会等待进程执行结束，直接执行下一个进程

    p.close()  # 关闭进程池，不再接受新的进程
    p.join()  # 等待进程池中的所有进程执行完毕。异步方式提交任务，一定要加上这句，否则主进程会在子进程执行完毕之前结束

    print('父进程执行结束')

"""
>>>
父进程开始执行
子进程开始执行： 1
子进程开始执行： 2
子进程开始执行： 3
子进程开始执行： 4
子进程执行结束： 1
子进程开始执行： 5
子进程执行结束： 3
子进程执行结束： 4
子进程执行结束： 2
子进程开始执行： 6
子进程开始执行： 8
子进程开始执行： 7
子进程执行结束： 5
子进程开始执行： 9
子进程执行结束： 6
子进程执行结束： 8
子进程执行结束： 7
子进程开始执行： 10
子进程执行结束： 9
子进程执行结束： 10
父进程执行结束
"""
