# 域名IP地址映射

- [Python] 域名转IP
```python
import socket

hostnames = [
    "mail.hundsun.com",
    "kfhsitsm.hundsun.com",
    "hs-cas.hundsun.com",
    "bp.hundsun.com",
    "oa.hundsun.com",
    "synergy.hundsun.com",
    "kh.hundsun.com",
    "doc.hundsun.com",
    "dev.hundsun.com",
    "hr.hundsun.com",
    "learning.hundsun.com",
    "home.hundsun.com",
    "interfacejump.hundsun.com",
    "package.hundsun.com"
]

for hostname in hostnames:
    try:
        ip_address = socket.gethostbyname(hostname)
        print(f"{ip_address:15} {hostname}")
    except socket.error as msg:
        print(f"# 0.0.0.0       {hostname}")

"""
执行: python script.py
结果:
39.170.59.162   mail.hundsun.com
192.168.66.123  kfhsitsm.hundsun.com
192.168.66.105  hs-cas.hundsun.com
192.168.66.123  bp.hundsun.com
# 0.0.0.0       oa.hundsun.com
192.168.66.96   synergy.hundsun.com
192.168.66.140  kh.hundsun.com
172.28.10.158   doc.hundsun.com
192.168.66.123  dev.hundsun.com
192.168.66.108  hr.hundsun.com
192.168.66.123  learning.hundsun.com
# 0.0.0.0       home.hundsun.com
# 0.0.0.0       interfacejump.hundsun.com
# 0.0.0.0       package.hundsun.com
"""
```

- [Python] IP转地址
```python
"""
安装依赖: pip install geoip2
下载数据: curl -fLo GeoLite2-City.mmdb https://github.com/xin053/ipd/blob/master/GeoLite2-City.mmdb # 从github下载，也可以从本地下载: \\HomeCloud\home\Drive\data\database\light\GeoLite2-City.mmdb
"""

import geoip2.database

# Open the GeoLite2 database
reader = geoip2.database.Reader('GeoLite2-City.mmdb')

# test baidu.com
response = reader.city('39.156.66.10') 
print(response, type(response))
print(response.country.name)


# test google.com
response = reader.city('172.217.160.78')  
print(response, type(response))
print(response.country.name)

"""
执行: python script.py
结果:
geoip2.models.City({'continent': {'code': 'AS', 'geoname_id': 6255147, 'names': {'de': 'Asien', 'en': 'Asia', 'es': 'Asia', 'fr': 'Asie', 'ja': 'アジア', 'pt-BR': 'Ásia', 'ru': 'Азия', 'zh-CN': '亚洲'}}, 'country': {'geoname_id': 1814991, 'iso_code': 'CN', 'names': {'de': 'China', 'en': 'China', 'es': 'China', 'fr': 'Chine', 'ja': '中国', 'pt-BR': 'China', 'ru': 'Китай', 'zh-CN': '中国'}}, 'location': {'accuracy_radius': 50, 'latitude': 34.7725, 'longitude': 113.7266}, 'registered_country': {'geoname_id': 1814991, 'iso_code': 'CN', 'names': {'de': 'China', 'en': 'China', 'es': 'China', 'fr': 'Chine', 'ja': '中国', 'pt-BR': 'China', 'ru': 'Китай', 'zh-CN': '中国'}}, 'traits': {'ip_address': '39.156.66.10', 'prefix_len': 15}}, ['en']) <class 'geoip2.models.City'>
China
geoip2.models.City({'city': {'geoname_id': 5375480, 'names': {'de': 'Mountain View', 'en': 'Mountain View', 'fr': 'Mountain View', 'ja': 'マウンテンビュー', 'ru': 'Маунтин-Вью', 'zh-CN': '芒廷维尤'}}, 'continent': {'code': 'NA', 'geoname_id': 6255149, 'names': {'de': 'Nordamerika', 'en': 'North America', 'es': 'Norteamérica', 'fr': 'Amérique du Nord', 'ja': '北アメリカ', 'pt-BR': 'América do Norte', 'ru': 'Северная Америка', 'zh-CN': '北美洲'}}, 'country': {'geoname_id': 6252001, 'iso_code': 'US', 'names': {'de': 'USA', 'en': 'United States', 'es': 'Estados Unidos', 'fr': 'États-Unis', 'ja': 'アメリカ合衆国', 'pt-BR': 'Estados Unidos', 'ru': 'США', 'zh-CN': '美国'}}, 'location': {'accuracy_radius': 1000, 'latitude': 37.419200000000004, 'longitude': -122.0574, 'metro_code': 807, 'time_zone': 'America/Los_Angeles'}, 'postal': {'code': '94043'}, 'registered_country': {'geoname_id': 6252001, 'iso_code': 'US', 'names': {'de': 'USA', 'en': 'United States', 'es': 'Estados Unidos', 'fr': 'États-Unis', 'ja': 'アメリカ合衆国', 'pt-BR': 'Estados Unidos', 'ru': 'США', 'zh-CN': '美国'}}, 'subdivisions': [{'geoname_id': 5332921, 'iso_code': 'CA', 'names': {'de': 'Kalifornien', 'en': 'California', 'es': 'California', 'fr': 'Californie', 'ja': 'カリフォル 
ニア州', 'pt-BR': 'Califórnia', 'ru': 'Калифорния', 'zh-CN': '加利福尼亚州'}}], 'traits': {'ip_address': '172.217.160.78', 'prefix_len': 17}}, ['en']) <class 'geoip2.models.City'>
United States
"""
```
