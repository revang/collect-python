# -*- coding: utf-8 -*-
import cx_Oracle
import os
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'

db=cx_Oracle.connect('xir_trd/xpar@127.0.0.1:1521/xvams')
cursor=db.cursor()

ref_cursor=cursor.var(cx_Oracle.CURSOR)
params=('2019-07-01',ref_cursor)
result=cursor.callproc('PKG_ACCI_REPORT.P_RPT_ACCI_1',params)[-1]
titles=[item[0] for item in result.description]
print(titles)
for row in result:
    print(row)

cursor.close()
db.close()