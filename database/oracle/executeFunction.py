# -*- coding: utf-8 -*-
import cx_Oracle
from pprint import pprint
import os
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'

conn=cx_Oracle.connect('xir_trd/xpar@127.0.0.1:1521/xvams2')
cursor=conn.cursor()
bond_name=cursor.callfunc('DEVELOP.PKG_ACCI_INSTRUMENT.F_BOND',cx_Oracle.STRING,('132013','SPT_BD','XSHG','BOND_NAME'))
print('债券名称：',bond_name)
cursor.close()
conn.close()
