# -*- coding: utf-8 -*-

"""
抓取蛋卷基金的数据
"""

import requests
import json
import database.sqlalchemy.sqlalchemy as db
import time
import random
import pandas as pd
import collections

def get_fund_json(fund_code,to_file=False):
    """抓取蛋卷基金数据"""
    url="https://danjuanapp.com/djapi/fund/detail/{}".format(fund_code)
    
    print("抓取: {}".format(fund_code))
    res=requests.get(url,headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36"})
    jsontext=res.text

    if to_file: # 写到本地 json 文件方便调试
        filename="./{}.json".format(fund_code)
        with open(filename,"w") as f:
            """ 
            json.dump(dict,fp) 把dict转换成str类型存到fp指向的文件里
            参数：indent=2 格式化json，缩进的位数为2
            参数：ensure_ascii=False 输出中文
            """
            json.dump(res.json(),f,indent=2,ensure_ascii=False)

    return jsontext

def parse_fund(fund_code,json_text):
    """解析基金信息：披露日期、基金名称、管理经理"""
    json_data=json.loads(json_text)
    data=json_data['data']
    manager_list=data['manager_list']
    achievement_list=manager_list[0]['achievement_list'] # 找到一个管理者

    try:
        init_date=data['fund_position']['enddate'].replace('-','')
    except KeyError:
        init_date=19000101
    fund_name=fund_name_from_manager_list(fund_code,achievement_list)
    manager=get_manager(manager_list)

    return init_date,fund_name,manager


def fund_name_from_manager_list(fund_code,achievement_list):
    """每个管理者都会管理很多基金，找到当前这个基金并返回名字"""
    for fund in achievement_list:
        if fund["fund_code"]==str(fund_code):
            return fund["fundsname"]
    return ""

def get_manager(manager_list):
    """找到所有基金管理人返回空格分割字符串 eg: 李晓星 张坤"""
    name_list=[]
    for manager in manager_list:
        name_list.append(manager['name'])
    return " ".join(name_list)

Connection=None
Table=None 

def init_conn():
    global Connection,Table 
    url="mysql+pymysql://dev:Welcome_1@192.168.137.80:3306/develop"
    engine=db.create_engine(url)
    metadata=db.MetaData()
    Connection=engine.connect()
    Table=db.Table('danjuan_fund',metadata,autoload=True,autoload_with=engine)

# 在 mysql 创建表
"""
CREATE TABLE `danjuan_fund` (
	  `init_date` varchar(32) NOT NULL DEFAULT '' COMMENT '季报日期',
		`fund_code` varchar(16) NOT NULL DEFAULT '' COMMENT '基金代码',
    `fund_name` varchar(64) DEFAULT '' COMMENT '基金名称',
    `manager` varchar(32) NOT NULL DEFAULT '' COMMENT '管理人',
    `detail_json` text NOT NULL COMMENT '蛋卷基金详细信息 json',
    PRIMARY KEY (`init_date`,`fund_code`),
    KEY `idx_code` (`fund_code`),
    KEY `idx_name` (`fund_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
"""

def save_mysql(init_date,fund_code,fund_name,manager,detail_json):
    query=db.insert(Table).values(
        init_date=init_date,
        fund_code=fund_code,
        fund_name=fund_name,
        manager=manager,
        detail_json=detail_json
    )
    Connection.execute(query)

def request_and_save(fund_code):
    json_text=get_fund_json(fund_code)
    init_date,fund_name,manager=parse_fund(fund_code,json_text)
    save_mysql(init_date,fund_code,fund_name,manager,json_text)


def get_my_xieqiu_fund_codes():
    """
    获取res：
    1、在浏览器找到连接，选择 Copy as cURL(bash)
    2、在base执行以下命令
        $ uncurl "<步骤1的内容>"
    """
    # res=requests.get("https://stock.xueqiu.com/v5/stock/portfolio/stock/list.json?size=1000&pid=-110&category=2",
    #     headers={
    #         "Accept": "application/json, text/plain, */*",
    #         "Accept-Language": "en,zh;q=0.9,zh-CN;q=0.8",
    #         "Connection": "keep-alive",
    #         "Origin": "https://xueqiu.com",
    #         "Referer": "https://xueqiu.com/",
    #         "Sec-Fetch-Dest": "empty",
    #         "Sec-Fetch-Mode": "cors",
    #         "Sec-Fetch-Site": "same-site",
    #         "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36"
    #     },
    #     cookies={}, # TODO 用浏览器查询请求，改成你自己的 uncurl requests 代码，注意你的 cookie 不要随便泄露出去
    # )

    # with open("./funds.json","w") as f:
    #     json.dump(res.json(),f,indent=2,ensure_ascii=False)

    codes=[] # [ (code, name) ]
    with open("./funds.json") as f:
        res=json.load(f)
        stocks=res["data"]["stocks"]
        for stock in stocks:
            symbol=stock["symbol"]
            fund_code="".join(char for char in symbol if char.isdigit())
            fund_name=stock["name"]
            codes.append((fund_code,fund_name))
    return codes 

def crawl_all_my_funds_to_mysql():
    funds=get_my_xieqiu_fund_codes()
    __import__('pprint').pprint(funds)

    for fund_code,fund_name in funds:
        request_and_save(fund_code)
        time.sleep(random.randint(5,10))  # 注意慢一点，随机 sleep 防止命中反作弊

def export_all_mysql_funds_stocks_to_dict():
    """导出所有基金的股票前十大重仓股票到 excel"""
    query = db.select([Table]).order_by(db.desc(Table.columns.fund_code)).limit(100)
    rows = Connection.execute(query).fetchall()
    fund_dict = {}
    for row in rows:
        d = json.loads(row.detail_json)
        try:
            stock_list = d['data']['fund_position']['stock_list']
        except KeyError:  # 新基金没披露可能为空
            stock_list = []

        stocks = []
        for stock in stock_list:
            name, code, percent = stock['name'], stock['code'], stock['percent']
            stock_fmt = u"{}[{}]({}%)".format(name, code, percent)
            stocks.append(stock_fmt)

        if len(stocks) < 10: # 十大重仓股
            stocks += (10 - len(stocks)) * [""]

        key = row.fund_name
        vals = [row.fund_code, row.manager, row.init_date] + stocks
        fund_dict[key] = vals

    return fund_dict

# https://www.geeksforgeeks.org/how-to-create-dataframe-from-dictionary-in-python-pandas/
def export_all_mysql_funds_stocks_to_excel_vertical():
    fund_dict = export_all_mysql_funds_stocks_to_dict()
    index = ['代码', '管理人', '季报日期'] + ['重仓股'] * 10  # 十大重仓
    df = pd.DataFrame(fund_dict, index=index)
    df.to_excel("./funds_stock_vertical.xlsx")


def export_all_mysql_funds_stocks_to_excel():  # 横着
    fund_dict = export_all_mysql_funds_stocks_to_dict()
    # index = ['代码', '管理人', '季报日期'] + ['重仓股'] * 10
    df = pd.DataFrame.from_dict(fund_dict, orient='index')
    df.to_excel("./fund_stock.xlsx")


def export_all_stock_funds():
    """导出每个股票被多少基金持有，比较容易看出哪些股票被抱团"""
    query = db.select([Table]).order_by(db.desc(Table.columns.fund_code)).limit(100)
    rows = Connection.execute(query).fetchall()
    stock_funds = collections.defaultdict(list)
    for row in rows:
        d = json.loads(row.detail_json)
        try:
            stock_list = d['data']['fund_position']['stock_list']
        except KeyError:  # 新基金没披露可能为空
            stock_list = []

        for stock in stock_list:
            name, code, percent = stock['name'], stock['code'], stock['percent']
            stock_name = u"{}({})".format(name, code)
            stock_funds[stock_name].append(row.fund_name)

    keys = sorted(stock_funds, key=lambda k: len(stock_funds[k]), reverse=True)
    sorted_stock_dict = {k: stock_funds[k] for k in keys}
    df = pd.DataFrame.from_dict(sorted_stock_dict, orient='index')
    df.to_excel("./stock.xlsx")

def main():
    # get_fund_json("007300", "汇添富中盘", True) # 单独抓取一个基金数据到文件
    # crawl_all_my_funds_to_mysql() # 抓取所有我关注的雪球上的基金到 mysql

    export_all_mysql_funds_stocks_to_excel_vertical()  # 导出基金十大重仓股
    export_all_mysql_funds_stocks_to_excel()  # 导出横版基金十大重仓

    export_all_stock_funds()  # 导出每个重仓股票分别被多少基金持有

if __name__ == "__main__":
    # get_fund_json("399001",True)

    # with open('./399001.json') as f:
    #     json_text=f.read()
    #     print(parse_fund(json_text))

    # init_conn()
    # request_and_save(399001)

    # get_my_xieqiu_fund_codes()
    # print(get_my_xieqiu_fund_codes())

    # init_conn()
    # crawl_all_my_funds_to_mysql()

    init_conn()
    main()