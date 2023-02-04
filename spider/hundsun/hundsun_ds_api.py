import requests


def json_to_csv(json_list, csv_name):
    import pandas as pd
    import os
    if not os.path.exists(csv_name):
        df = pd.DataFrame(json_list)
        df.to_csv(csv_name, index=False, encoding="utf-8")
    else:
        df = pd.DataFrame(json_list)
        df.to_csv(csv_name, header=False, index=False,  encoding="utf-8", mode="a")


def spider_hundsun_ds_api(url_list, csv_path):
    for url in url_list:
        try:
            response = requests.get(url,
                                    headers={
                                        "Accept": "application/json, text/javascript, */*; q=0.01",
                                        "Accept-Language": "zh-CN,zh;q=0.9",
                                        "Connection": "keep-alive",
                                        "Referer": "http://wm-eca.hundsun.com/custom/manage/pieInit?superiorsys=%E6%96%B0%E7%94%B5%E5%95%86%E5%B9%B3%E5%8F%B0",
                                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
                                        "X-Requested-With": "XMLHttpRequest"
                                    },
                                    cookies={
                                        "JSESSIONID": "node0r57f2xoi9idv1rh87ti3orasw10132.node0",
                                        "b3222f5ad5658c1a_gdp_cs1": "wugm34577",
                                        "b3222f5ad5658c1a_gdp_esid": "4584",
                                        "b3222f5ad5658c1a_gdp_gio_id": "wugm34577",
                                        "color": "grey",
                                        "gdp_user_id": "2e2057a1-2d7d-49e9-8501-2fd1a6e669fb"
                                    },
                                    auth=(),
                                    verify=False
                                    )
            # print(response.text)
            json_dict = response.json()
            json_list = json_dict["rows"]
            json_to_csv(json_list, "hundsun_ds_api_newdsplatform.csv")
            print(f"execute {url} success")
        except:
            print(f"execute {url} failed")


# 1. 新电商平台 共2044 ---> 50*41
url_list = [f"http://wm-eca.hundsun.com/custom/manage/queryInterface?superiorSys=%E6%96%B0%E7%94%B5%E5%95%86%E5%B9%B3%E5%8F%B0&page={x}&rows=50" for x in range(1, 42)]
spider_hundsun_ds_api(url_list, "新电商平台.csv")
