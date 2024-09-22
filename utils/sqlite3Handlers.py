# 导入相关模块
import json
import os
import sqlite3
from datetime import datetime
import pytz

from .filePathHelper import NoDuplicateFile, EnsureFolders


class Sqlite3Handler:
    temp_log_table = "temp_log"
    touch_log_table = "touch_log"
    error_log_table = "error_log"
    db_path = './data/records/'
    db_name = 'BoevxaDb.db'
    db_path_name = db_path + db_name
    newFile = False

    # 使用 __init__ 初始化数据 的话，使用一次 Sqlite3Handler() 会执行一次，如：type(Sqlite3Handler())
    def InitSqlite3(self, db_path='', db_name='BoevxaDb.db'):
        # print('__int__')
        if len(db_path.strip()) > 1:
            self.db_path = EnsureFolders(db_path)
        self.db_name = db_name
        self.db_path_name = NoDuplicateFile(self.db_path, self.db_name,".db")
        print('sqlite3 :', self.db_path_name)
        # con = sqlite3.connect(":memory:")  # 表示在内存中创建的数据库文件，运行完数据即丢失
        # 连接到SQLite数据库
        # 可以指定创建数据库的路径，比如可以写成sqlite3.connect(r"E:\DEMO.db")
        # 如果文件不存在，会自动在当前目录创建:
        # , isolation_level = None) 这样，对应的代码就不再需要commit() 操作了
        self.conn = sqlite3.connect(self.db_path_name, isolation_level=None)
        # print('self.conn ', self.conn)
        # 创建一个Cursor:
        self.cursor = self.conn.cursor()
        # print('self.cursor', self.cursor)
        print("连接 sqlite3 成功！！", self.cursor)
        # self.CreateTempLogTable()
        self.CreateTouchLogTable()
        self.CreateErrorLogTable()

    def CreateTempLogTable(self, temp_log_table=''):
        if len(temp_log_table.strip()) > 1:
            self.temp_log_table = temp_log_table
        try:
            # 创建数据表成功
            sql = f'''CREATE TABLE IF NOT EXISTS `{self.temp_log_table}`(
                              `id` INTEGER PRIMARY KEY AUTOINCREMENT,
                              `hex_temp` TEXT,
                              `dec_temp` INTEGER UNSIGNED,
                              `brightness` INTEGER UNSIGNED,
                              `create_time` TIMESTAMP NOT NULL DEFAULT (strftime('%Y-%m-%d %H:%M:%f','now','localtime')));
                           '''
            self.cursor.execute(sql)
            return 1
        except Exception as e:
            print('>> Create Temp Log Table Error:', e)
            return 0

    def CreateTouchLogTable(self, touch_log_table=''):
        if len(touch_log_table.strip()) > 1:
            self.touch_log_table = touch_log_table
        try:
            # 创建数据表成功
            sql = f'''CREATE TABLE IF NOT EXISTS `{self.touch_log_table}`(
                           `id` INTEGER PRIMARY KEY AUTOINCREMENT,
                           `signal` INTEGER,
                           `count` INTEGER UNSIGNED,
                           `points` TEXT,
                           `create_time` TIMESTAMP NOT NULL DEFAULT (strftime('%Y-%m-%d %H:%M:%f','now','localtime')));
                        '''
            self.cursor.execute(sql)
            return 1
        except Exception as e:
            print('>> Create Log Table Error:', e)
            return 0

    def CreateErrorLogTable(self, error_log_table=''):
        if len(error_log_table.strip()) > 1:
            self.error_log_table = error_log_table
        try:
            # 创建数据表成功
            sql = f'''CREATE TABLE IF NOT EXISTS `{self.error_log_table}`(
                           `id` INTEGER PRIMARY KEY AUTOINCREMENT,
                           `function` TEXT,
                           `operate` TEXT,
                           `data` TEXT,
                           `message` TEXT,
                           `create_time` TIMESTAMP NOT NULL DEFAULT (strftime('%Y-%m-%d %H:%M:%f','now','localtime')));
                        '''
            self.cursor.execute(sql)
            return 1
        except Exception as e:
            print('>> Create Error Log Table Error:', e)
            return 0

    def InsertTempLog(self, hex_temp, dec_temp, brightness):
        # 继续执行一条SQL语句，插入一条记录:  test
        try:
            sql = f'''INSERT INTO {self.temp_log_table} (hex_temp, dec_temp, brightness) 
            VALUES (?, ?, ?)'''
            self.cursor.execute(sql, (hex_temp, dec_temp, brightness))
            return self.cursor.lastrowid
        except Exception as e:
            print('>> Insert Touch Log Error:', e)
            self.InsertErrorLog(function='InsertTempLog', operate='INSERT',
                                data=f'(hex_temp, dec_temp, brightness)={hex_temp}, {dec_temp}, {brightness}', message=str(e))
            return 0

    def InsertTouchLog(self, signal, count, points):
        # 继续执行一条SQL语句，插入一条记录:  test
        try:
            sql = f'''INSERT INTO {self.touch_log_table} (signal,count,points) 
            VALUES (?, ?, ?)'''
            self.cursor.execute(sql, (signal, count, points))
            return self.cursor.lastrowid
        except Exception as e:
            print('>> Insert Touch Log Error:', e)
            self.InsertErrorLog(function='InsertTouchLog', operate='INSERT',
                                data=f'(signal, count, points)={signal}, {count}, {points}', message=str(e))
            return 0

    def InsertErrorLog(self, function, operate, data, message: str):
        # 继续执行一条SQL语句，插入一条记录:  test
        try:
            self.ReconnectDb()
            sql = f'''INSERT INTO {self.error_log_table} (function,operate,data,message) 
            VALUES (?, ?, ?, ?)'''
            self.cursor.execute(sql, (function, operate, data, message[-512:-1]))
            return self.cursor.lastrowid
        except Exception as e:
            print('>> Insert Error Log Table Error:', e)
            self.InsertErrorLog(function='InsertErrorLog', operate='INSERT',
                                data=f'(function, operate, data)={function}, {operate}, {data}', message=str(e))
            return 0

    # 修复更新数据比插入数据块（问题点：更行数据时，没有找到新数据，更新就变成了插入一行新数据）
    def SelectTouchLog(self, select_id):  # 查询方式三：根据多个查询条件获取表中某几列的数据 and points is null
        self.cursor.execute(f"SELECT id,points FROM {self.touch_log_table} WHERE id = ?",
                            (select_id,))
        result = self.cursor.fetchall()
        return result

    def UpdateTouchLog(self, search_id, filed, value):
        try:
            # 方式一
            self.cursor.execute(f"UPDATE {self.touch_log_table} SET {filed}=? WHERE id=?", (value, search_id))
            return self.cursor.lastrowid
        except Exception as e:
            print('>> Update Touch Log Error:', e)
            self.InsertErrorLog(function='UpdateTouchLog', operate='UPDATE',
                                data=f'(search_id, filed, value)={search_id}, {filed}, {value}', message=str(e))
            return 0

    def ReconnectDb(self):
        self.cursor.close()
        self.conn.close()
        self.conn = sqlite3.connect(self.db_path_name, isolation_level=None)
        self.cursor = self.conn.cursor()
        print("重新 连接 sqlite3 成功！！", self.cursor)

    def SelectAllTouchLog(self):
        sql = f"SELECT * from {self.touch_log_table};"
        self.cursor.execute(sql)
        res = self.cursor.fetchall()
        return res

    def __del__(self):
        try:
            # 关闭Cursor:
            self.cursor.close()
            # 提交事务:
            self.conn.commit()
            # 关闭Connection:
            self.conn.close()
            print('保存 sqlite3 成功！！')
        except Exception as e:
            pass


# 程序入口
if __name__ == '__main__':
    sqlite3Handler = Sqlite3Handler()
    sqlite3Handler.InitSqlite3()
    # sqlite3Handler.InsertTouchLog(signal=1, count=10, points='(1,3)/(2,4)/(3,4)/')
    # res = sqlite3Handler.SelectALL()
    # print(res)
    # sqlite3Handler.UpdateData(search_id=10, filed='count', value=11)
    # dbID = sqlite3Handler.InsertTouchLog(signal=9, count=None, points=None)
    # print(dbID)
    # result = sqlite3Handler.SelectTouchLog(select_id=6)
    for i in range(10):
        sqlite3Handler.InsertTempLog(hex_temp=0x11, dec_temp=123,brightness=20)
        sqlite3Handler.InsertTempLog(hex_temp='0x11', dec_temp=123.3,brightness=40)
        # sqlite3Handler.UpdateTouchLog(search_id=6, filed='count', value='22')
        # sqlite3Handler.UpdateTouchLog(search_id=6, filed='points', value='(a,b),(c,d)')
    # print(result)
    # print(len(result))
