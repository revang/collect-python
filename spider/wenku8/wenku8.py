import requests
from bs4 import BeautifulSoup

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36'}
cookies = {}
params = {"action": "login", "username": "dujiaoshou", "password": "dujiaoshou801"}  # form data


def login():
    global cookies
    response = requests.post("https://www.wenku8.net/login.php", headers=headers, params=params)
    cookies = response.cookies.get_dict()
    cookies["jieqiUserCharset"] = "big5"  # 不加会乱码
    print(cookies)


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


login()
get_book_list()
