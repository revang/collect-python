import requests
import json
import time
import pandas as pd
from print_color import printGreen,printRed

pd.set_option('display.unicode.ambiguous_as_wide',True)
pd.set_option('display.unicode.east_asian_width',True)


def get_fund_daily_quotes(fund_code):
    """抓取基金日行情数据"""
    res=requests.get("https://danjuanapp.com/djapi/fund/estimate-nav/{}".format(fund_code),
        headers={
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "en,zh;q=0.9,zh-CN;q=0.8",
            "Connection": "keep-alive",
            "Referer": "https://danjuanapp.com/funding/100053?channel=1300100141",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36",
            "elastic-apm-traceparent": "00-260b51cbcc725a042ba6b247ba333f9b-d6ee500443c835ad-01"
        },
        cookies={
            "Hm_lpvt_b53ede02df3afea0608038748f4c9f36": "1604292806",
            "Hm_lvt_b53ede02df3afea0608038748f4c9f36": "1604229911,1604291718,1604292706,1604292806",
            "acw_tc": "2760776d16042917186951031ef72dad6dd5f66977a697cbf98b12314869ef",
            "channel": "1300100141",
            "device_id": "web_Sklduzh_P",
            "timestamp": "1604292808094",
            "xq_a_token": "c2974070ad952835feab798d5278f70696c9f25c"
        },
    )
    jsondata=json.loads(res.text)

    item=jsondata["data"]["items"][-1]
    init_date=time.strftime("%Y-%m-%d",time.localtime(item["time"]/1000))
    fund_code=fund_code
    fund_name=get_fund_name(fund_code)
    update_time=time.strftime("%H:%M:%S",time.localtime(item["time"]/1000))
    percentage=item["percentage"]

    fund_daily_quotes={}
    fund_daily_quotes["init_date"]=init_date
    fund_daily_quotes["fund_code"]=fund_code
    fund_daily_quotes["fund_name"]=fund_name
    fund_daily_quotes["update_time"]=update_time
    fund_daily_quotes["percentage"]=percentage
    return fund_daily_quotes

def get_fund_name(fund_code):
    res=requests.get('https://danjuanapp.com/djapi/fund/{}'.format(fund_code),
        headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36'}
    )
    json_data=json.loads(res.text)

    fund_name=json_data['data']['fd_name']
    return fund_name

def main():
    """
    我关注的基金：
    2020-11-02 005918 天弘沪深300ETF联接C 13:58:00 0.7689
    2020-11-02 100053 富国上证综指ETF联接 13:58:00 0.1783
    2020-11-02 110003 易方达上证50指数A 13:58:00 -0.19
    2020-11-02 399001 中海上证50指数增强 13:58:00 -0.19
    2020-11-02 000961 天弘沪深300ETF联接A 13:58:00 0.741
    2020-11-02 005919 天弘中证500指数C 13:58:00 0.75
    2020-11-02 000404 易方达新兴成长 13:58:00 1.0801
    2020-11-02 001513 易方达信息产业混合 13:58:00 0.4342
    2020-11-02 519674 银河创新混合 13:58:00 1.1691
    2020-11-02 320007 诺安成长混合 13:58:00 2.5102
    2020-11-02 161903 万家行业优选混合 13:58:00 3.1367
    2020-11-02 260108 景顺长城新兴成长 13:58:00 1.0103
    2020-11-02 519005 海富通股票混合 13:58:00 -0.3978
    2020-11-02 005911 广发双擎升级混合 13:58:00 1.3139
    2020-11-02 001480 财通成长优选混合 13:57:00 0.9858
    2020-11-02 161726 招商生物医药 13:58:00 -1.5295
    2020-11-02 000727 融通健康产业混合 13:58:00 -0.6674
    2020-11-02 001875 前海开源沪港深优势精选 13:58:00 0.6291
    2020-11-02 006751 富国互联科技股票 13:58:00 1.4589
    2020-11-02 110011 易方达中小盘混合 13:58:00 0.3722
    2020-11-02 162703 广发小盘成长混合（LOF） 13:58:00 1.2578
    2020-11-02 161028 富国中证新能源汽车指数分级 13:58:00 3.7525
    2020-11-02 001790 国泰智能汽车股票 13:58:00 3.121
    2020-11-02 110022 易方达消费行业 13:58:00 1.4173
    2020-11-02 000083 汇添富消费行业混合 13:58:00 -0.0105
    2020-11-02 161725 招商中证白酒指数 13:58:00 2.1945
    2020-11-02 001071 华安媒体互联网混合 13:58:00 0.3129
    2020-11-02 001595 天弘中证银行指数C 13:58:00 -0.0856
    2020-11-02 001552 天弘中证证券保险指数A 13:58:00 -0.399
    2020-11-02 167301 方正富邦中证保险主题指数分级 13:58:00 -0.8718
    2020-11-02 002979 广发金融地产联接C 13:57:00 -0.195
    2020-11-02 164907 交银中证互联网金融指数 13:58:00 -0.7426
    """
    fund_list=["005918","100053","110003","399001","000961","005919",
        "000404","001513","519674","320007","161903","260108","519005","005911","001480","161726","000727","001875","006751","110011","162703","161028","001790",
        "110022","000083","161725","001071","001595","001552","167301","002979","164907"
    ]

    fund_daily_quotes_list=[]
    for fund in fund_list:
        fund_daily_quotes_list.append(get_fund_daily_quotes(fund))
    
    # print("查询日期 基金代码 基金名称 更新时间 涨跌幅(%)")
    # for fund_daily_quotes in fund_daily_quotes_list:
    #     if fund_daily_quotes["percentage"]>=0:
    #         printRed("{} {} {} {} {}".format(fund_daily_quotes["init_date"], fund_daily_quotes["fund_code"], fund_daily_quotes["fund_name"], fund_daily_quotes["update_time"], fund_daily_quotes["percentage"]))
    #     else:
    #         printGreen("{} {} {} {} {}".format(fund_daily_quotes["init_date"], fund_daily_quotes["fund_code"], fund_daily_quotes["fund_name"], fund_daily_quotes["update_time"], fund_daily_quotes["percentage"]))

    df = pd.DataFrame(fund_daily_quotes_list)
    df1 = df.sort_values("percentage", ascending=False)
    df1.index=range(len(df1))
    print(df1)
    
if __name__ == "__main__":
    main()



