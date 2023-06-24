import jaydebeapi

class PhoenixDBUtil:
    """
    Phoenix数据库操作工具类
    """

    def __init__(self, url: str, driver_class: str):
        self._url = url
        self._driver_class = driver_class
        self._connection = None
        self._cursor = None

    def conn(self):
        """
        建立连接
        """
        if self._connection is None:
            self._connection = jaydebeapi.connect(self._driver_class, self._url)

    def close(self):
        """
        关闭连接
        """
        if self._cursor is not None:
            self._cursor.close()

        if self._connection is not None:
            self._connection.close()

    def execute(self, sql: str):
        """
         执行SQL语句，通用方法，返回全部数据
         :param sql: SQL语句
         """
        
        # 使用conn方法获取连接对象和游标对象。
        self.conn()
        
        self._cursor = self._connection.cursor()
        self._cursor.execute(sql)

        result_set = self.fetch_all()

        return result_set

    def fetch_all(self):
        # 获取全部数据，并返回结果集。
        return [row for row in self]

    def __iter__(self):
        # 迭代器方法，用于逐行读取SQL执行结果。
        try:
            while True:
                row = self.next()
                yield row    
        except StopIteration:
            pass

    def next(self):
        # 读取下一行数据。
        return tuple(map(str, next(self._cursor)))
    
    def execute_update(self, sql: str):
        """
        执行SQL语句，用于执行更新操作，如insert、update和delete等。
        :param sql: SQL语句
        """
        
        # 使用conn方法获取连接对象和游标对象。
        self.conn()
        
        self._cursor = self._connection.cursor()
        self._cursor.execute(sql)
        
    def create_table(self, table_name: str, column_families: dict):
        """
        创建表格
        :param table_name: 表名
        :param column_families: 列族，字典类型，键为列族名，值为列族配置参数
        """
        
        sql = f"CREATE TABLE {table_name} ("
        for cf in column_families.keys():
            sql += f"{cf} map<varchar, varchar="">, "
            
        sql = sql.rstrip(", ") + ")"
        
        self.execute_update(sql)

    def insert_table(self, table_name: str, data_dict: dict):
        """
        插入数据到表格中
        :param table_name: 表名
        :param data_dict: 数据，字典类型，键为列族名：列限定符，值为数据值
        """

        sql = f"UPSERT INTO {table_name} ("
        for k in data_dict.keys():
            cf, cq = k.split(":")
            sql += f"{cf}.{cq}, "
        
        sql = sql.rstrip(", ") + ") VALUES ("
        
        for v in data_dict.values():
            sql += f"'{v}', "
        
        sql = sql.rstrip(", ") + ")"
        
        self.execute_update(sql)

    def delete_table(self, table_name: str, row_key: str):
        """
         删除表格中的某一行数据
         :param table_name: 表名
         :param row_key: 行键
         """
         
        sql = f"DELETE FROM {table_name} WHERE ROWKEY = '{row_key}'"
        
        self.execute_update(sql)

    def select_table(self, table_name: str, row_key: str):
        """
        查询表格中的某一行数据
        :param table_name: 表名
        :param row_key: 行键
        """
        
        sql = f"SELECT * FROM {table_name} WHERE ROWKEY = '{row_key}'"
        
        result_set = self.execute(sql)
        
        if len(result_set) > 0:
            return result_set[0]
            
        return None

    def drop_table(self, table_name: str):
        """
         删除表格
         :param table_name: 表名
         """

        sql = f"DROP TABLE IF EXISTS {table_name}"

        self.execute_update(sql)

    def __del__(self):
        # 在对象被销毁时，如果连接还存在，则关闭连接。
        self.close()