import requests
from scrapy.spiders import CrawlSpider
from scrapy.http import Request
from xueqiu.items import XueqiuItem


class XueqiuSpider(CrawlSpider):
    name = "xueqiu"
    allowed_domains = ["xueqiu.com"]
    start_urls = ["https://stock.xueqiu.com/v5/stock/chart/minute.json?symbol=SH600570&period=1d"]

    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36"}
    cookies = {}

    def login(self):
        response = requests.get("https://xueqiu.com", headers=self.headers, verify=False)
        self.cookies = response.cookies.get_dict()

    def start_requests(self):
        self.login()
        for url in self.start_urls:
            yield Request(url, headers=self.headers, cookies=self.cookies, callback=self.parse)

    def parse(self, response):
        print(response.text[:100], "...")
        json_dict = response.json()
        json_list = json_dict['data']['items']
        for item in json_list:
            xueqiu_item = XueqiuItem()
            xueqiu_item['stock_code'] = "SH600570"
            xueqiu_item['current_price'] = item['current']
            xueqiu_item['percent'] = item['percent']
            yield xueqiu_item
