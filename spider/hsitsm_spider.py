# -*- coding: utf-8 -*-
import requests
from collections import namedtuple
from tqdm import tqdm
from oracledb import OracleDB


Event = namedtuple('Event', ('event_no', 'product_name', 'title', 'content', 'solution', 'accept_time'))

headers = {'Content-Type': 'application/json;charset=UTF-8'}
cookies = {'token': 'ab7e99a7-e7e9-4b0f-8242-e518938c74774'}
db = OracleDB()


pages = requests.post('https://kfhsitsm.hundsun.com/itsm/business/v/event/selectPage', headers=headers, cookies=cookies, data=str({'query_req': {'product_id': [], 'page_num': 1, 'page_size': 100}}).encode()).json()['data']['pages']
print("total pages:", pages)
# for curr_page in tqdm(range(1, pages+1)):
#     try:
#         events = []
#         response = requests.post('https://kfhsitsm.hundsun.com/itsm/business/v/event/selectPage', headers=headers, cookies=cookies, data=str({'query_req': {'product_id': [], 'page_num': curr_page, 'page_size': 100}}).encode())
#         json_data = response.json()
#         for item in json_data['data']['list']:
#             events.append(Event(item['event_no'], item['product_name'], str(item['title']).strip(), str(item['content']).strip(), str(item['solution']).strip(), item['accept_time']))
#         db.insertmany("insert into event (event_no, product_name, title, content, solution, accept_time) values (:event_no, :product_name, :title, :content, :solution, :accept_time)", events)
#     except:
#         pass
    