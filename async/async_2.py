import asyncio
import time


async def get_page(url):
    print('正在下载：', url)
    await asyncio.sleep(2)
    print('下载成功：', url)
    return f"source_{url}"

url_list = ['http://www.baidu.com', 'http://www.sina.com', 'http://www.163.com', 'http://www.tencent.com', 'http://www.alibaba.com']
task_list = []

for url in url_list:
    coroutine = get_page(url)  # 创建协程对象
    task = asyncio.ensure_future(coroutine)  # 将协程包装成一个任务对象
    task_list.append(task)  # 将任务对象添加到任务列表中

loop = asyncio.get_event_loop()  # 创建一个事件循环对象
time1 = time.time()
loop.run_until_complete(asyncio.wait(task_list))  # 将任务列表中的任务全部添加到事件循环中
time2 = time.time()-time1
print(time2)

"""
>>>
正在下载： http://www.baidu.com
正在下载： http://www.sina.com
正在下载： http://www.163.com
正在下载： http://www.tencent.com
正在下载： http://www.alibaba.com
下载成功： http://www.baidu.com
下载成功： http://www.163.com
下载成功： http://www.alibaba.com
下载成功： http://www.sina.com
下载成功： http://www.tencent.com
2.016719102859497
"""

"""
第5行代码中不能使用time模块来模拟I/O阻塞，因为time模块不支持异步，如果使用time模块，执行时间就会延长。>>> async def get_page(url): await asyncio.sleep(2)
这里使用的是asyncio模块的sleep()函数，但是注意需要加上await关键词进行修饰，让代码等待I/O操作完成再进行下一步。如果不使用await关键词修饰I/O操作，执行时间就会接近0秒，其中的任务未完成就结束了，这样无意义。
第15行代码也需要使用asyncio模块的wait()函数将任务列表逐个注册到事件循环对象中，不能直接使用列表注册，否则会报错。
"""
