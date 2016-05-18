#coding:utf-8
import random
import sqlite3
import threading

from utils.concurent.thread_utils import run_in_background

# 全局锁，多数据库共享，待改进，改为带数据库单锁，
mutex = threading.Lock()


def new_table(db_name, table_name, column_sql):
    execute(db_name, 'create table if not exists ' + table_name + ' (' + column_sql + ')')


def execute(db_name, sql):
    mutex.acquire()
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute(sql)
    # print(cursor.rowcount)
    cursor.close()
    conn.commit()
    conn.close()
    mutex.release()


def query(db_name, sql_fmt, *args):
    mutex.acquire()
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute(sql_fmt, *args)
    values = cursor.fetchall()
    cursor.close()
    conn.close()
    mutex.release()
    return values


def test_new_table():
    new_table('test.db', 'user', 'id varchar(20), name varchar(20)')


def test_insert():
    execute('test.db', 'insert into user (id, name) values (\'' + str(random.randint(0, 100)) + '\', \'test' + str(
        random.randint(0, 100)) + '\')')


def test_query():
    print(query('test.db', 'select * from user'))


if __name__ == '__main__':
    test_new_table()
    for i in range(9):
        if i % 2 == 0:
            run_in_background(test_query)
        else:
            run_in_background(test_insert)
