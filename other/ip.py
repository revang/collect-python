"""
pip install geoip2

注意: 由于GeoLite2-City.mmdb文件较大, 项目中未包含。下载地址: https://github.com/xin053/ipd/blob/master/GeoLite2-City.mmdb
"""

import geoip2.database

# Open the GeoLite2 database
reader = geoip2.database.Reader('GeoLite2-City.mmdb')

# Look up an IP address
# response = reader.city('8.8.8.8')
# response = reader.city('39.156.66.10') # baidu.com
response = reader.city('172.217.160.78')  # google.com

# Print the location information
print(response.country.name)
print(response.subdivisions.most_specific.name)
print(response.city.name)
print(response.postal.code)
print(response.location.latitude, response.location.longitude)
