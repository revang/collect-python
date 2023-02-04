import requests
import time
import re
import os
from datetime import datetime
from bs4 import BeautifulSoup
from lxml import etree


class LiuliArticle:
    pass


class LiuliSpider:
    def __init__(self):
        self.proxies = {"http": "http://localhost:1081", "https": "http://localhost:1081"}
        self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36"}
        self.articledic = {}

    def article_list(self, url):
        """
        获取文章列表

        >>> liuli = LiuliSpider()
        >>> print(liuli.article_list("https://www.hacg.mom/wp/comic.html/page/1"))
        {'liuli_94672': {'id': 'liuli_94672', 'title': 'かじむらマーケット(かじむらカジマ)こづくりおねだりドウターズ', 'cover': 'https: //2021.liuli.app/22123001.jpg', ...}, ...}
        """
        def format_title(title):
            title = re.sub(r"\s+", "", title)  # 去除空白字符
            return title

        def format_description(description):
            description = re.sub(r"\s+", "", description)
            description = description.replace("继续阅读", "")
            description = description.replace("→", "")
            return description

        response = requests.get(url, headers=self.headers, proxies=self.proxies)
        response.encoding = "utf-8"

        ret = {}
        soup = BeautifulSoup(response.text, "html.parser")
        elements = soup.find_all("article", {"id": re.compile("^post-\d+$")})  # 获取id为post-的元素列表
        for element in elements:
            id = element["id"].replace("post-", "liuli_")  # 获取元素的属性
            title = format_title(element.find("h1", {"class": "entry-title"}).get_text())  # 获取元素文本
            cover = element.find("img")["src"]
            categories = "/".join([e.get_text() for e in element.find("span", {"class": "cat-links"}).find_all("a")])
            tags = "/".join([e.get_text() for e in element.find("span", {"class": "tag-links"}).find_all("a")])
            description = format_description(element.find("div", {"class": "entry-content"}).get_text())
            search_url = url
            detail_url = element.find("h1", {"class": "entry-title"}).find("a")["href"]
            create_time = datetime.strptime(element.find("time")["datetime"], "%Y-%m-%dT%H:%M:%S%z").strftime("%Y-%m-%d %H:%M:%S")

            article = {id: {"id": id, "title": title, "cover": cover, "categories": categories, "tags": tags, "description": description, "search_url": search_url, "detail_url": detail_url, "create_time": create_time}}
            ret.update(article)

        self.articledic.update(ret)
        return ret

    def article_detail(self, id):
        """
        获取文章详情

        >>> liuli = LiuliSpider()
        >>> print(liuli.article_detail("liuli_94672"))
        {'id': 'liuli_94672', ..., 'magnet': 'magnet:?xt=urn:btih:0A274679AFE1DDB27F8352BA2D4D95BECF30320B', 'content': '毁三观的本子...'}
        """
        def format_content(content):
            content = re.sub(r"\s+", "", content)
            return content

        article = self.articledic[id]

        response = requests.get(article["detail_url"], headers=self.headers, proxies=self.proxies)
        response.encoding = "utf-8"

        soup = BeautifulSoup(response.text, "html.parser")
        element = soup.find("div", {"class": "entry-content"})
        article["magnet"] = "magnet:?xt=urn:btih:"+re.compile(r"[a-zA-Z0-9]{40}").findall(str(element))[0]
        article["content"] = format_content("".join([e.get_text() for e in element.find_all("p")]))

        self.articledic[id] = article

        return article
