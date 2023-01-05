from threading import Thread
import time
import random


def task(url_list):
    try:
        print(random.choice(url_list))
        time.sleep(2)
    except Exception as e:
        print(e)


if __name__ == '__main__':
    print("main start")

    thread_list = []  # 线程列表
    url_list = []  # url列表
    for i in range(10):  # 生成10个url
        url_list.append("http://www.baidu.com/{}".format(i))

    start_time = time.time()
    for i in range(10):  # 生成10个线程
        t = Thread(target=task, args=(url_list,))  # 创建线程
        t.start()  # 启动线程
        thread_list.append(t)

    for t in thread_list:
        t.join()  # 等待所有线程执行完毕

    print("cost time: {}".format(time.time() - start_time))
    print("main end")

'''
>>>
main start
http://www.baidu.com/6
http://www.baidu.com/8
http://www.baidu.com/0
http://www.baidu.com/4
http://www.baidu.com/5
http://www.baidu.com/3
http://www.baidu.com/0
http://www.baidu.com/9
http://www.baidu.com/5
http://www.baidu.com/9
cost time: 2.0100629329681396
main end
'''
