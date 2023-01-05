import os


def get_sql_file_list(target_path):
    """
    获取目标文件夹下的sql文件
    sql文件类型
        - sql ---> sql 
        - pck ---> package   包
        - prc ---> procedure 存储过程
        - fnc ---> function  函数
        - trg ---> trigger   触发器
    """
    sql_file_list = []
    for root, dirs, files in os.walk(target_path):
        for filename in files:
            if filename.endswith(('.sql', '.pck', '.prc', '.fnc', '.trg')) and filename[0:10] != "SQLExecute":
                sql_file_list.append(os.path.join(root, filename))
    return sql_file_list


if __name__ == "__main__":
    file_list = get_sql_file_list(os.getcwd())
    execute_file = "SQLExecute.sql"
    with open(execute_file, "w") as f:
        for filepath in file_list:
            f.write("prompt executing '{}'\n".format(filepath))
            f.write("                @'{}'\n".format(filepath))
