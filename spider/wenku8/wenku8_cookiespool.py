import requests
import random
import json
from bs4 import BeautifulSoup

"""
建立Cookie池

目的: 
1. 为了避免被封账号
    在爬虫程序中使用cookie模拟登录是为了爬取那些需要登录才能获取的数据。如果使用同一个账号登录网站频繁爬取数据，有可能被服务器察觉，服务器就会封禁这个账号。
    对于这种反爬措施，也可以采用和IP反爬措施相同的应对思路：不同账号的cookie值是不同的，使用多个账号登录网站并记录cookie值，将这些cookie值保存在一个cookie池中，在爬取数据时从cookie池中随机选取一个cookie值用于登录，就能降低账号被封禁的概率。

2. cookie值具有时效性
    在指定时间之后cookie值就过期了，因此，在每一次使用cookie池之前，最好都调用一下get_cookies()函数来获取最新的cookie值。

3. 不同的账号登录网站后，看到的网页内容是不同的
    例如，有些网站会根据用户的登录状态来显示不同的网页内容，这些内容可能包含了一些敏感信息，如果使用同一个账号登录网站，就会导致这些敏感信息被爬取到，这是不安全的。
"""


headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36'}
cookies_list = []
user_list = [{"username": "dujiaoshou", "password": "dujiaoshou801"}, {"username": "dujiaoshou", "password": "dujiaoshou801"}]


def get_cookies():
    global cookies_list
    for user in user_list:
        params = {"action": "login", "username": user["username"], "password": user["password"]}  # params = {"action": "login", "username": "dujiaoshou", "password": "dujiaoshou801"}  # plyload / form data
        response = requests.post("https://www.wenku8.net/login.php", headers=headers, params=params)
        cookies = response.cookies.get_dict()
        cookies["jieqiUserCharset"] = "big5"  # 不加会乱码
        cookies_list.append(cookies)

    for i, cookies in enumerate(cookies_list, 1):
        print(i, json.dumps(cookies)[:100]+"...")


def get_book_list():
    """
    获取书籍列表(我的书架)

    原始请求
    requests.get("https://www.wenku8.net/modules/article/bookcase.php",
                headers={
                    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                    "accept-language": "zh-CN,zh;q=0.9",
                    "authority": "www.wenku8.net",
                    "cache-control": "max-age=0",
                    "if-none-match": "1672946025|340702",
                    "sec-ch-ua": "\"Not?A_Brand\";v=\"8\", \"Chromium\";v=\"108\", \"Google Chrome\";v=\"108\"",
                    "sec-ch-ua-mobile": "?0",
                    "sec-ch-ua-platform": "\"Windows\"",
                    "sec-fetch-dest": "document",
                    "sec-fetch-mode": "navigate",
                    "sec-fetch-site": "none",
                    "sec-fetch-user": "?1",
                    "upgrade-insecure-requests": "1",
                    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
                },
                cookies={
                    "Hm_lpvt_d72896ddbf8d27c750e3b365ea2fc902": "1672946027",
                    "Hm_lvt_d72896ddbf8d27c750e3b365ea2fc902": "1672944996",
                    "PHPSESSID": "5c0fukjhroe99a6p6k2gm39efp2o1hpo",
                    "__51uvsct__1xpAUPUjtatG3hli": "1",
                    "__51vcke__1xpAUPUjtatG3hli": "83758f71-e1cb-53b0-b4be-f363f4336e4e",
                    "__51vuft__1xpAUPUjtatG3hli": "1672945371432",
                    "__vtins__1xpAUPUjtatG3hli": "%7B%22sid%22%3A%20%22d54246de-365f-5085-874a-203069526f75%22%2C%20%22vd%22%3A%205%2C%20%22stt%22%3A%20165373%2C%20%22dr%22%3A%2067188%2C%20%22expires%22%3A%201672947336801%2C%20%22ct%22%3A%201672945536801%7D",
                    "jieqiUserCharset": "big5",
                    "jieqiUserInfo": "jieqiUserId%3D340702%2CjieqiUserName%3Ddujiaoshou%2CjieqiUserGroup%3D3%2CjieqiUserVip%3D0%2CjieqiUserName_un%3Ddujiaoshou%2CjieqiUserHonor_un%3D%26%23x65B0%3B%26%23x624B%3B%26%23x4E0A%3B%26%23x8DEF%3B%2CjieqiUserGroupName_un%3D%26%23x666E%3B%26%23x901A%3B%26%23x4F1A%3B%26%23x5458%3B%2CjieqiUserLogin%3D1672945556",
                    "jieqiVisitInfo": "jieqiUserLogin%3D1672945556%2CjieqiUserId%3D340702"
                },
                auth=(),
                )
    """
    cookies = random.choice(cookies_list)  # 随机选择一个账号
    response = requests.get("https://www.wenku8.net/modules/article/bookcase.php", headers=headers, cookies=cookies)
    response.encoding = "big5"
    htm_text = response.text
    # with (open("bookcase.html", "w", encoding="utf-8")) as f:
    #     f.write(response.text)
    # with open("bookcase.html", "r", encoding="utf-8") as f:
    #     htm_text = f.read()

    soup = BeautifulSoup(htm_text, "html.parser")
    book_list = soup.find("table", {"class": "grid"}).find_all("tr")
    book_list = [book for book in book_list if book.find("td", {"class": "even"})]  # 子元素存在 <td class="even">

    for idx, book in enumerate(book_list, 1):
        try:
            elements = book.find_all("td")
            title = elements[1].find("a").get_text()
            author = elements[2].find("a").get_text()
            update_date = elements[5].get_text().strip()
            print(f"{idx}. {title}, {author}, {update_date}")
        except Exception as e:
            print(e)


get_cookies()
get_book_list()
