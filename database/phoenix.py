import jaydebeapi


class PhoenixDBUtil:
    def __init__(self, url):
        self.conn = jaydebeapi.connect("org.apache.phoenix.jdbc.PhoenixDriver", url, {'phoenix.schema.isNamespaceMappingEnabled': 'true', 'phoenix.schema.mapSystemTablesToNamespace': 'true'}, 'lib/phoenix-client-hbase-2.4.0-5.1.3.jar')

    def execute(self, sql):
        cursor = self.conn.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()
        return result

    # def create_table(self, table_name, columns):
    #     column_definition = ", ".join([f"{column} VARCHAR" for column in columns])
    #     sql = f"CREATE TABLE {table_name} ({column_definition})"
    #     return self.execute(sql)

    # def insert_table(self, table_name, values):
    #     value_strs = [f"('{value}')" for value in values]
    #     sql_values = ", ".join(value_strs)
    #     sql = f"UPSERT INTO {table_name} VALUES {sql_values}"
    #     return self.execute(sql)

    def select_table(self, table_name):
        sql = f"SELECT * FROM {table_name}"
        return self.execute(sql)

    # def delete_table(self, table_name):
    #     sql = f"DELETE FROM {table_name}"
    #     return self.execute(sql)

    # def drop_table(self, table_name):
    #     sql = f"DROP TABLE {table_name}"
    #     return self.execute(sql)
