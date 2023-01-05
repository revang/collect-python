from multiprocessing import Process
import time

"""
进程的创建

第二种方法是直接使用Process类，将执行爬虫任务的函数的名称作为参数target的值，其他参数以元组或字典的格式传入。演示代码如下：
"""


def test(url1):
    print('子进程开始执行：', url1)
    time.sleep(2)
    print('子进程执行结束：', url1)


if __name__ == '__main__':
    print('父进程开始执行')
    p1 = Process(target=test, args=('url1',))
    p2 = Process(target=test, args=('url2',))
    p1.start()
    p2.start()
    p1.join()
    p2.join()
    print('父进程执行结束')

"""
>>>
父进程开始执行
子进程开始执行： url1
子进程开始执行： url2
子进程执行结束： url2
子进程执行结束： url1
父进程执行结束
"""
