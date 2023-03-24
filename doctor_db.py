'''
    操作doctor表，涉及操作依次为插入、删除、查询
'''
#encoding: utf-8
import psycopg2

def insert(id, password):
    conn = psycopg2.connect(database="vaccine_ms",user="postgres",password="",host="127.0.0.1",port="5432")
    cur = conn.cursor()
    change_id = '\'' + id + '\''
    change_password = '\'' + password + '\''
    sql= 'insert into doctor values (' + change_id + ',' + change_password + ')'
    print(sql)
    cur.execute(sql)
    conn.commit()
    print('插入成功')

def delete(input_id_card):
    conn = psycopg2.connect(database="vaccine_ms",user="postgres",password="",host="127.0.0.1",port="5432")
    cur = conn.cursor()
    change_id = '\'' + input_id_card + '\''
    sql = 'delete from doctor where id = ' + change_id
    print(sql)
    cur.execute(sql)
    conn.commit()
    print('删除成功')

def select(input_id, input_password):
    conn = psycopg2.connect(database="vaccine_ms",user="postgres",password="",host="127.0.0.1",port="5432")
    cur = conn.cursor()
    change_id = '\'' + input_id + '\''
    change_password = '\'' + input_password + '\''
    sql = 'select * from doctor where id = ' + change_id + ' AND ' + 'password = ' + change_password
    print(sql)
    cur.execute(sql)
    conn.commit()
    # cur.fetchall()获取查询结果
    get_data = cur.fetchall()
    return get_data