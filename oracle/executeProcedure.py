# -*- coding: utf-8 -*-
import cx_Oracle
import os
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'

conn = cx_Oracle.connect('xir_trd/xpar@127.0.0.1:1521/xvams')
cursor = conn.cursor()

o_status = cursor.var(cx_Oracle.NUMBER)
o_memo = cursor.var(cx_Oracle.STRING)
params = ('2019-06-30', '2019-07-01', o_status, o_memo)
cursor.callproc('PKG_ACCI_TASK.P_INSTRUMENT_GENERATE', params)

print("RESULT: {}; MEMO: {};".format(o_status.getvalue(), o_memo.getvalue()))

cursor.close()
conn.close()
