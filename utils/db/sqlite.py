import sqlite3


def new_table(db_name, table_name, column_sql):
    execute(db_name, 'create table if not exists ' + table_name + ' (' + column_sql + ')')


def execute(db_name, sql):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute(sql)
    # print(cursor.rowcount)
    cursor.close()
    conn.commit()
    conn.close()


def query(db_name, sql_fmt, *args):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute(sql_fmt, *args)
    values = cursor.fetchall()
    cursor.close()
    conn.close()
    return values


def test_new_table():
    new_table('test.db', 'req', 'id varchar(20) primary key, name varchar(20)')


def test_insert():
    execute('test.db', 'insert into user (id, name) values (\'3\', \'test1\')')


def test_query():
    print(query('test.db', 'select * from user where id=?', ('1',)))

if __name__ == '__main__':
    test_insert()
