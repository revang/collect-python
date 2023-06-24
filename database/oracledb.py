#!/usr/bin/env python
# -*- coding:utf-8 -*-

import cx_Oracle as oracledb
import logging
# from app.utils import loadconfig

"""
pip install cx_Oracle
"""

logging.basicConfig(level=logging.ERROR, format="%(asctime)s %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
logger = logging.getLogger()


class OracleDB:
    def __init__(self, database_name=None):
        """ 
        初始化数据库连接 

        :param database_name 数据库连接配置名称
        :return: None
        """
        # database_conf = loadconfig(database_name)
        # username = database_conf["Username"]
        # password = database_conf["Password"]
        # host = database_conf["Host"]
        # port = database_conf["Port"]
        # database = database_conf["Database"]

        self.connect_conf = "alex/alex@192.168.50.195:11521/vctpdb"

    def conn(self):
        """ 连接数据库 """
        self.db = oracledb.connect(self.connect_conf)
        self.cursor = self.db.cursor()

    def close(self):
        """ 关闭数据库 """
        self.cursor.close()
        self.db.close()

    def queryone(self, sql, return_rowtype="tuple"):
        """ 查询单行 
        :param sql            SQL脚本
        :param return_rowtype 返回行类型 enumerate=["tuple","dict"]
        :return list[tuple]/list[dict]
        """
        if return_rowtype not in ("tuple", "dict"):
            raise ValueError(f"invaild return_rowtype: {return_rowtype}")

        if return_rowtype == "tuple":
            self.conn()
            logger.debug(sql)
            self.cursor.execute(sql)
            row = self.cursor.fetchone()
            self.close()
            return row

        if return_rowtype == "dict":
            self.conn()
            logger.debug(sql)
            self.cursor.execute(sql)
            self.cursor.rowfactory = lambda *args: dict(zip([d[0].lower() for d in self.cursor.description], args))
            row = self.cursor.fetchone()

            # 判断是否有lob类型, 如果有, 则转换成string
            lob_columns = [key for key, val in row.items() if isinstance(val, oracledb.LOB)]
            if len(lob_columns) != 0:
                for key, val in row.items():
                    if isinstance(val, oracledb.LOB):
                        row[key] = val.read()
            self.close()
            return row

    def queryfirstvalue(self, sql):
        """ 
        查询第一个值

        :param sql SQL脚本
        :return:   任意数据类型
        """
        # return list(self.queryone(sql))[0]
        return None

    def query(self, sql, row_type="tuple"):
        if row_type not in ("tuple", "dict"):
            raise ValueError(f"invaild row_type: {row_type}")

        if row_type == "tuple":
            self.conn()
            logger.debug(sql)
            self.cursor.execute(sql)
            rows = self.cursor.fetchall()
            self.close()
            return rows

        if row_type == "dict":
            self.conn()
            logger.debug(sql)
            self.cursor.execute(sql)
            self.cursor.rowfactory = lambda *args: dict(zip([d[0].lower() for d in self.cursor.description], args))
            rows = self.cursor.fetchall()

            # 判断是否有lob类型, 如果有, 则转换成string
            lob_columns = [key for key, val in rows[0].items() if isinstance(val, oracledb.LOB)] if len(rows) != 0 else []
            if len(lob_columns) != 0:
                for row in rows:
                    for column in lob_columns:
                        row[column] = str(row[column])  # lob从内存中读取数据
            self.close()
            return rows

    def query_chunk(self, sql, row_type="tuple", chunksize=None):
        if row_type not in ("tuple", "dict"):
            raise ValueError(f"invaild row_type: {row_type}")

        if row_type == "tuple":
            self.conn()
            logger.debug(sql)
            self.cursor.execute(sql)
            rows = self.cursor.fetchmany(numRows=chunksize)
            while len(rows) != 0:
                yield rows
                rows = self.cursor.fetchmany(numRows=chunksize)
            self.close()
            return

        if row_type == "dict":
            self.conn()
            logger.debug(sql)
            self.cursor.execute(sql)
            self.cursor.rowfactory = lambda *args: dict(zip([d[0].lower() for d in self.cursor.description], args))
            rows = self.cursor.fetchmany(numRows=chunksize)
            # 判断是否有lob类型, 如果有, 则转换成string
            lob_columns = [key for key, val in rows[0].items() if isinstance(val, oracledb.LOB)] if len(rows) != 0 else []
            if len(lob_columns) != 0:
                for row in rows:
                    for column in lob_columns:
                        row[column] = str(row[column])  # lob从内存中读取数据
            while len(rows) != 0:
                yield rows
                rows = self.cursor.fetchmany(numRows=chunksize)
                # 判断是否有lob类型, 如果有, 则转换成string
                lob_columns = [key for key, val in rows[0].items() if isinstance(val, oracledb.LOB)] if len(rows) != 0 else []
                if len(lob_columns) != 0:
                    for row in rows:
                        for column in lob_columns:
                            row[column] = str(row[column])  # lob从内存中读取数据
            self.close()
            return

    def callfunc(self, function_name, return_type, params):
        self.conn()
        res = self.cursor.callfunc(function_name, return_type, params)
        self.close()
        return res

    def querydml(self, object_type, object_name):
        return self.callfunc("dbms_metadata.get_ddl", str, [object_type, object_name])

    def is_exist_table(self, schema_name, table_name):
        return self.queryfirstvalue(f"select count(1) from all_tables where owner = upper('{schema_name}') and table_name = upper('{table_name}')") == 1

    def show(self, sql):
        """ 
        显示
        """
        self.conn()
        logger.debug(sql)
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        self.close()
        for row in rows:
            print(row)

    def __execute(self, sql, params=None):
        """
        执行单行
        """
        if params is None:
            self.conn()
            logger.debug(sql)
            self.cursor.execute(sql)
            self.db.commit()
            count = self.cursor.rowcount
            self.close()
            return count
        else:
            self.conn()
            logger.debug(sql)
            logger.debug(params)
            self.cursor.execute(sql, params)
            self.db.commit()
            count = self.cursor.rowcount
            self.close()
            return count

    def __executemany(self, sql, rows):
        """
        执行多行(用于多行插入)
        注意: 由于cursor.executemany没有返回值, 本函数没有返回值

        :param sql  SQL脚本
        :param rows 数据集  extra: data_type=list[dict]
        :return:    None
        """
        self.conn()
        logger.debug(sql)
        # logger.debug(rows)
        self.cursor.executemany(sql, rows)
        self.db.commit()
        # count = self.cursor.getarraydmlrowcounts()
        self.close()
        return

    def __executequeue(self, sql_list):
        """
        执行SQL列表

        :param sql_list SQL列表 extra: data_type=list[dict]
        :return:        None
        """
        self.conn()
        for sql in sql_list:
            logger.debug(sql)
            self.cursor.execute(sql)
        self.db.commit()
        self.close()

    def insert(self, sql, row=None):
        """
        插入单行
        """
        return self.__execute(sql, row)

    def insertmany(self, sql, rows=None):
        """
        插入多行
        """
        self.__executemany(sql, rows)

    def update(self, sql, params=None):
        """
        更新
        """
        return self.__execute(sql, params)

    def delete(self, sql, params=None):
        """
        删除
        """
        return self.__execute(sql, params)

    def execute(self, sql, params=None):
        """
        执行单行
        """
        self.__execute(sql, params)

    def executequeue(self, sql_list):
        """
        执行队列
        """
        self.__executequeue(sql_list)
