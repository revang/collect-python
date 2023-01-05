import asyncio
import time


async def get_page(url):  # 使用async定义一个协程, 协程是一个特殊的函数, 可以使用await关键字挂起阻塞的操作, 比如IO操作, 网络请求等
    print('正在下载：', url)
    await asyncio.sleep(2)
    print('下载成功：', url)
    return f"source_{url}"


def parse_page(task):  # 回调函数
    print('正在解析：', task.result())  # task.result()为绑定回调函数的get_page()函数的返回值


coroutine = get_page('http://www.baidu.com')  # 创建协程对象

"""
然后将协程对象进一步封装为任务对象。任务对象可以使用回调函数，在爬虫应用中很重要，因为回调函数会在任务函数之后执行。
假设在爬虫应用中任务函数是对网址发起请求，回调函数是对请求的网页源代码进行数据解析，网址请求完毕后再调用数据解析的回调函数，数据解析完毕，一个网址的爬虫任务才算完成。
如果不使用回调函数，对网址发起请求的函数不知道数据解析何时完毕，当前协程何时结束，需要对数据解析函数进行轮询，这样效率就比较低。因此，在事件驱动型程序中，回调函数是比较常用的。
"""

task = asyncio.ensure_future(coroutine)  # 将协程包装成一个任务对象
task.add_done_callback(parse_page)  # 为任务对象添加回调函数

"""
接着创建事件循环对象。事件循环是asyncio模块的核心，它可以执行异步任务、事件回调、网络I/O操作及运行子进程。
使用事件循环能以异步的方式高效地执行事件循环对象中的任务对象，提高爬虫代码的执行效率
"""
loop = asyncio.get_event_loop()  # 创建事件循环对象
loop.run_until_complete(task)  # 将任务对象注册到事件循环对象中，并启动事件循环对象

"""
>>>
正在下载： http://www.baidu.com
下载成功： http://www.baidu.com
正在解析： source_http://www.baidu.com
"""
