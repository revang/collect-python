import json
import time
import concurrent.futures
from threading import Thread
import requests

# 兴全-个人信息
# response = requests.get("https://m.xqfunds.com/appServer/account/account/queryAccoinfo.json?jsonpCallback=queryAccoinfoCallBack_1673910196561&querybankinfo=false&channel=mobileweb&_=1673910196377",
#                         headers={
#                             "Accept": "text/javascript, application/javascript, application/ecmascript, application/x-ecmascript, */*; q=0.01",
#                             "Accept-Language": "zh-CN,zh;q=0.9",
#                             "Connection": "keep-alive",
#                             "Referer": "https://m.xqfunds.com/pages/account-info.html",
#                             "Sec-Fetch-Dest": "empty",
#                             "Sec-Fetch-Mode": "cors",
#                             "Sec-Fetch-Site": "same-origin",
#                             "User-Agent": "Mozilla/5.0 (Linux; Android 8.0.0; SM-G955U Build/R16NW) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Mobile Safari/537.36",
#                             "X-Requested-With": "XMLHttpRequest",
#                             "sec-ch-ua": "\"Not_A Brand\";v=\"99\", \"Google Chrome\";v=\"109\", \"Chromium\";v=\"109\"",
#                             "sec-ch-ua-mobile": "?1",
#                             "sec-ch-ua-platform": "\"Android\""
#                         },
#                         cookies={
#                             "BIGipServerm5_http_pool_ipv6": "3036891146.20480.0000",
#                             "Hm_lpvt_dcb516e3c274642766105c07af1508c9": "1673910162",
#                             "Hm_lvt_dcb516e3c274642766105c07af1508c9": "1673906756",
#                             "SESSION": "YzI0NDNhYjQtZTNjNi00YjRiLWJmMTMtN2I5OWQ5ZGYwNDNj",
#                             "clientid": "e463df1ee3078adf1887b0446b659c70tqyectyejawqaqbtjqcq",
#                             "tokene463df1ee3078adf1887b0446b659c70tqyectyejawqaqbtjqcq": "H53CCHVERNIM15FVCC5GBMNGMBEW3I2B"
#                         },
#                         # auth=(),
#                         )

# print(response.text)

# 兴全-投资收益
# response = requests.get("https://m.xqfunds.com/appServer/query/share/dcInvestProfitQueryGroup.json?jsonpCallback=dcInvestProfitCallback2_1673937120116&supportsupermoneythirdshare=true&containsshareintrans=false&supportsupermoney=true&transfiltersp=true&queryintrans=true&supportIiaShare=true&channel=mobileweb&_=1673937119970",
#                         headers={
#                             # "Accept": "text/javascript, application/javascript, application/ecmascript, application/x-ecmascript, */*; q=0.01",
#                             # "Accept-Language": "zh-CN,zh;q=0.9",
#                             # "Connection": "keep-alive",
#                             # "Referer": "https://m.xqfunds.com/pages/asset.html",
#                             # "Sec-Fetch-Dest": "empty",
#                             # "Sec-Fetch-Mode": "cors",
#                             # "Sec-Fetch-Site": "same-origin",
#                             "User-Agent": "Mozilla/5.0 (Linux; Android 8.0.0; SM-G955U Build/R16NW) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Mobile Safari/537.36",
#                             # "X-Requested-With": "XMLHttpRequest",
#                             # "sec-ch-ua": "\"Not_A Brand\";v=\"99\", \"Google Chrome\";v=\"109\", \"Chromium\";v=\"109\"",
#                             # "sec-ch-ua-mobile": "?1",
#                             # "sec-ch-ua-platform": "\"Android\""
#                         },
#                         cookies={
#                             # "BIGipServerm5_http_pool_ipv6": "3036891146.20480.0000",
#                             # "Hm_lpvt_dcb516e3c274642766105c07af1508c9": "1673910967",
#                             # "Hm_lvt_dcb516e3c274642766105c07af1508c9": "1673906756",
#                             "SESSION": "MTExM2YxNzUtZjdiZS00YzNlLWJlY2EtYzQ4NTE2NGVkOWNj",  # key
#                             # "clientid": "e463df1ee3078adf1887b0446b659c70tqyectyejawqaqbtjqcq",
#                             # "tokene463df1ee3078adf1887b0446b659c70tqyectyejawqaqbtjqcq": "I6P0H7LBZ8XVKMAJ8H61P4BU6L2P75KM"
#                         },
#                         auth=(),
#                         )
# print(response.text)

from datetime import datetime


def clock(func):
    """
    计算函数运行时间装饰器

    >>> import time
    >>>
    >>> @clock
    >>> def hello():
    >>>     time.sleep(3)
    >>>     print("Hello World")
    >>>
    >>> hello()
    Hello World
    function: hello, execute time: 3.0029s
    """
    def wrapper(*args, **kwargs):
        begin_time = datetime.now().timestamp()
        res = func(*args, **kwargs)
        end_time = datetime.now().timestamp()
        execute_time = end_time-begin_time
        print(f"function: {func.__name__}, execute time: {execute_time:.4f}s")
        return res
    return wrapper


class DateTimeUtil:

    @staticmethod
    def current_datetime():
        """
        获取当前时间datetime对象
        >>> cur = DateTimeUtil.current_datetime()
        >>> print(cur, type(cur))
        2023-01-03 03:03:40.098162 <class 'datetime.datetime'>
        """
        return datetime.now()

    @staticmethod
    def current_timestamp():
        """
        获取当前时间戳

        >>> cur = DateTimeUtil.current_timestamp()
        >>> print(cur, type(cur))
        1672686220 <class 'int'>
        """
        return int(datetime.now().timestamp())

    @staticmethod
    def current_strtime():
        """
        获取当前时间字符串

        >>> cur = DateTimeUtil.current_strtime()
        >>> print(cur, type(cur))
        2023-01-03 03:03:40 <class 'str'>
        """
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    @staticmethod
    def current_strdate():
        """
        获取当前日期字符串

        >>> cur = DateTimeUtil.current_strdate()
        >>> print(cur, type(cur))
        2023-01-03 <class 'str'>
        """
        return datetime.now().strftime('%Y-%m-%d')

    @staticmethod
    def datetime_to_timestamp(dt):
        """
        datetime对象转时间戳

        >>> dt = datetime.now()
        >>> cur = DateTimeUtil.datetime_to_timestamp(dt)
        >>> print(cur, type(cur))
        1672686220 <class 'int'>
        """
        return int(dt.timestamp())

    @staticmethod
    def timestamp_to_datetime(ts):
        """
        时间戳转datetime对象

        >>> cur = DateTimeUtil.timestamp_to_datetime(1672686220)
        >>> print(cur, type(cur))
        2023-01-03 03:03:40 <class 'datetime.datetime'>
        """
        return datetime.fromtimestamp(ts)

    @staticmethod
    def datetime_to_strtime(dt):
        """
        datetime对象转时间字符串

        >>> dt = datetime.now()
        >>> cur = DateTimeUtil.datetime_to_strtime(dt)
        >>> print(cur, type(cur))
        2023-01-03 03:03:40 <class 'str'>
        """
        return dt.strftime('%Y-%m-%d %H:%M:%S')

    @staticmethod
    def datetime_to_strdate(dt):
        """
        datetime对象转日期字符串

        >>> dt = datetime.now()
        >>> cur = DateTimeUtil.datetime_to_strdate(dt)
        >>> print(cur, type(cur))
        2023-01-03 <class 'str'>
        """
        return dt.strftime('%Y-%m-%d')

    @staticmethod
    def strtime_to_datetime(st):
        """
        时间字符串转datetime对象

        >>> cur = DateTimeUtil.strtime_to_datetime('2023-01-03 03:03:40')
        >>> print(cur, type(cur))
        2023-01-03 03:03:40 <class 'datetime.datetime'>
        """
        return datetime.strptime(st, '%Y-%m-%d %H:%M:%S')

    @staticmethod
    def strdate_to_datetime(sd):
        """
        日期字符串转datetime对象

        >>> cur = DateTimeUtil.strdate_to_datetime('2023-01-03')
        >>> print(cur, type(cur))
        2023-01-03 00:00:00 <class 'datetime.datetime'>
        """
        return datetime.strptime(sd, '%Y-%m-%d')

    @staticmethod
    def strtime_to_timestamp(st):
        """
        时间字符串转时间戳

        >>> cur = DateTimeUtil.strtime_to_timestamp('2023-01-03 03:03:40')
        >>> print(cur, type(cur))
        1672686220 <class 'int'>
        """
        return int(DateTimeUtil.strtime_to_datetime(st).timestamp())

    @staticmethod
    def strdate_to_timestamp(sd):
        """
        日期字符串转时间戳

        >>> cur = DateTimeUtil.strdate_to_timestamp('2023-01-03')
        >>> print(cur, type(cur))
        1672686220 <class 'int'>
        """
        return int(DateTimeUtil.strdate_to_datetime(sd).timestamp())

    @staticmethod
    def timestamp_to_strtime(ts):
        """
        时间戳转时间字符串

        >>> cur = DateTimeUtil.timestamp_to_strtime(1672686220)
        >>> print(cur, type(cur))
        2023-01-03 03:03:40 <class 'str'>
        """
        return DateTimeUtil.timestamp_to_datetime(ts).strftime('%Y-%m-%d %H:%M:%S')

    @staticmethod
    def timestamp_to_strdate(ts):
        """
        时间戳转日期字符串

        >>> cur = DateTimeUtil.timestamp_to_strdate(1672686220)
        >>> print(cur, type(cur))
        2023-01-03 <class 'str'>
        """
        return DateTimeUtil.timestamp_to_datetime(ts).strftime('%Y-%m-%d')


def request_investincome(i):
    begin_time = datetime.now().timestamp()
    # url = "https://m.xqfunds.com/appServer/query/share/dcInvestProfitQueryGroup.json?jsonpCallback=dcInvestProfitCallback2_1673937120116&supportsupermoneythirdshare=true&containsshareintrans=false&supportsupermoney=true&transfiltersp=true&queryintrans=true&supportIiaShare=true&channel=mobileweb&_=1673937119970"
    url = "https://m.xqfunds.com/appServer/query/share/dcInvestProfitQueryGroup.json?jsonpCallback=dcInvestProfitCallback2_1673942544746&supportsupermoneythirdshare=true&containsshareintrans=false&supportsupermoney=true&transfiltersp=true&queryintrans=true&supportIiaShare=true&channel=mobileweb&_=1673942544055&clientid=18025868"  # &clientid=18025868
    headers = {"User-Agent": "Mozilla/5.0 (Linux; Android 8.0.0; SM-G955U Build/R16NW) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Mobile Safari/537.36"}
    cookies = {"SESSION": "YzgyMmUzMTAtZjFkNi00ZDg0LTgwNTAtOGRmMTFmNzVhZmIx"}
    response = requests.get(url, headers=headers, cookies=cookies)

    status_code = response.status_code
    end_time = datetime.now().timestamp()
    execute_time = end_time-begin_time
    try:
        asset = json.loads(response.text[38:-1])["totalcapital"]
    except:
        print("error")
        print(response.text)
        asset = 0
    # print(f"status: {status_code}, {DateTimeUtil.timestamp_to_strtime(begin_time)}~{DateTimeUtil.timestamp_to_strtime(end_time)}, execute time: {execute_time:.4f}s")
    ctx = f"status: {status_code}, asset: {asset}, {DateTimeUtil.timestamp_to_strtime(begin_time)}~{DateTimeUtil.timestamp_to_strtime(end_time)}, execute time: {execute_time:.4f}s"
    return i, ctx


# thread_list = []
# url_list = [
#     "https://m.xqfunds.com/appServer/query/share/dcInvestProfitQueryGroup.json?jsonpCallback=dcInvestProfitCallback2_1673937120116&supportsupermoneythirdshare=true&containsshareintrans=false&supportsupermoney=true&transfiltersp=true&queryintrans=true&supportIiaShare=true&channel=mobileweb&_=1673937119970" for _ in range(10)]

# # start_time = time.time()
# for i in range(3):  # 生成10个线程
#     t = Thread(target=test_investincome, args=(url_list,))  # 创建线程
#     t.start()  # 启动线程
#     thread_list.append(t)

# for t in thread_list:
#     t.join()  # 等待所有线程执行完毕

# # print("cost time: {}".format(time.time() - start_time))
# print("main end")

# start_time = time.time()

# with concurrent.futures.ThreadPoolExecutor() as executor:
#     results = [executor.submit(request_investincome, i) for i in range(2)]
#     for f in concurrent.futures.as_completed(results):
#         # print(f.result())
#         i, ctx = f.result()
#         print(f"{i} - {ctx}")

# end_time = time.time()
# print(f'Took {end_time - start_time} seconds.')

i, ctx = request_investincome("")
print(ctx)
