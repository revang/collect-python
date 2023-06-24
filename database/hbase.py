import happybase

class HBaseDBUtil:
    """
    HBase数据库操作工具类
    """

    def __init__(self, host='localhost', port=9090):
        self._host = host
        self._port = port
        self._conn = None

    def conn(self):
        """
        建立连接
        """
        if self._conn is None or self._conn.closed:
            self._conn = happybase.Connection(host=self._host, port=self._port)

    def close(self):
        """
        关闭连接
        """
        if self._conn is not None and not self._conn.closed:
            self._conn.close()

    def create_table(self, table_name: str, column_families: dict):
        """
        创建表格
        :param table_name: 表名
        :param column_families: 列族，字典类型，键为列族名，值为列族配置参数
        """
        self.conn()
        self._conn.create_table(table_name, column_families)

    def insert_table(self, table_name: str, row_key: str, data_dict: dict):
        """
        插入数据到表格中
        :param table_name: 表名
        :param row_key: 行键
        :param data_dict: 数据，字典类型，键为列族名：列限定符，值为数据值
        """
        self.conn()
        table = self._conn.table(table_name)
        table.put(row_key.encode(), data_dict)

    def delete_table(self, table_name: str, row_key: str):
        """
        删除表格中的某一行数据
        :param table_name: 表名
        :param row_key: 行键
        """
        self.conn()
        table = self._conn.table(table_name)
        table.delete(row_key)

    def select_table(self, table_name: str, row_key: str):
        """
        查询表格中的某一行数据
        :param table_name: 表名
        :param row_key: 行键
        """
        self.conn()
        table = self._conn.table(table_name)
        return table.row(row_key)

    def drop_table(self, table_name: str):
        """
        删除表格
        :param table_name: 表名
        """
        self.conn()
        self._conn.delete_table(table_name, disable=True)
    
    def __del__(self):
        """
        在对象被销毁时，如果连接还存在，则关闭连接。
        """
        self.close()