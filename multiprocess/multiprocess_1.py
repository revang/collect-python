from multiprocessing import Process
import time


"""
进程的创建

第一种方法是新建一个继承自Process（进程）类的类，在类中定义run()函数，然后使用start()函数开启主进程，再由主进程调用类的run()函数来开启子进程。
"""


class MyProcess(Process):
    def __init__(self, name):
        super().__init__()
        self.name = name

    def run(self):
        print('子进程开始执行：', self.name)
        time.sleep(2)
        print('子进程执行结束：', self.name)


if __name__ == '__main__':
    print('父进程开始执行')
    p1 = MyProcess('p1')
    p2 = MyProcess('p2')
    p1.start()
    p2.start()
    p1.join()
    p2.join()
    print('父进程执行结束')

""" 
>>>
父进程开始执行
子进程开始执行： p1
子进程开始执行： p2
子进程执行结束： p1
子进程执行结束： p2
父进程执行结束 
"""
