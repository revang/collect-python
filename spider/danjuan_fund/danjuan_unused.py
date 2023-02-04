#-*- coding: utf-8 -*-

import requests
import json
from database.sqlalchemy.sqlalchemy import create_engine, Column, String, Integer, Float
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class FundConstituentStock(Base):
    __tablename__='fund_constituent_stock'

    init_date=Column(Integer(),primary_key=True)
    fund_code=Column(String(20),primary_key=True)
    fund_name=Column(String(64))
    stock_code=Column(String(20),primary_key=True)
    stock_name=Column(String(64))
    stock_price=Column(Float)
    stock_percent=Column(Float)

    def __init__(self,init_date,fund_code,fund_name,stock_code,stock_name,stock_price,stock_percent):
        self.init_date=init_date
        self.fund_code=fund_code
        self.fund_name=fund_name
        self.stock_code=stock_code
        self.stock_name=stock_name
        self.stock_price=stock_price
        self.stock_percent=stock_percent

def insert(stock_list):
    engine = create_engine('oracle://scott:tiger@192.168.137.91:1521/orcl', echo=False)  
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    for stock in stock_list:
        session.add(stock)
    session.commit()
    session.close()


def get_fund_constituent_stock_list(fund_code):
    url='https://danjuanapp.com/djapi/fund/detail/{}'.format(fund_code)
    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36'}

    res=requests.get(url,headers=headers)
    json_data=json.loads(res.text)

    # 基金成分股信息
    stock_list=[]
    for item in json_data['data']['fund_position']['stock_list']:
        init_date=json_data['data']['fund_position']['enddate'].replace('-','')
        fund_code=json_data['data']['fund_date_conf']['fd_code']
        fund_name=get_fund_name(fund_code)
        stock_code=item['code']
        stock_name=item['name']
        stock_price=item['current_price'] if 'current_price' in item else ''
        stock_percent=item['percent']

        stock_list.append(FundConstituentStock(init_date,fund_code,fund_name,stock_code,stock_name,stock_price,stock_percent))
    
    return stock_list

def get_fund_name(fund_code):
    url='https://danjuanapp.com/djapi/fund/{}'.format(fund_code)
    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36'}

    res=requests.get(url,headers=headers)
    json_data=json.loads(res.text)

    fund_name=json_data['data']['fd_name']

    return fund_name


if __name__ == "__main__":
    fund_list=['399001']

    fund_constituent_stock_list=[]
    for fund in fund_list:
        fund_constituent_stock_list=fund_constituent_stock_list+get_fund_constituent_stock_list(fund)
    
    insert(fund_constituent_stock_list)
   
