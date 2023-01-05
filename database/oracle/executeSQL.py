# -*- coding: utf-8 -*-
import cx_Oracle
import os
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'

conn = cx_Oracle.connect('xir_trd/xpar@127.0.0.1:1521/xvams')
cursor = conn.cursor()

sql="""SELECT T.I_CODE,T.A_TYPE,T.M_TYPE,T.B_NAME
 FROM XIR_MD.TBND T
WHERE T.I_CODE=:I_CODE 
  AND T.A_TYPE=:A_TYPE 
  AND T.M_TYPE=:M_TYPE
"""
params = {"I_CODE": "132013", "A_TYPE": "SPT_BD", "M_TYPE": "XSHG"}
cursor.execute(sql,params)
titles=[item[0] for item in cursor.description]
print(titles)
for row in cursor.fetchall():
  print(row)
cursor.close()
conn.close()
