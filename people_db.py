#encoding: utf-8
'''
    操作people表，涉及操作依次为插入、删除、查询、修改数据(两步组成：先删除，再插入)
'''
import psycopg2

def insert(id_card,name,sex,tele,situ):
    conn = psycopg2.connect(database="vaccine_ms",user="postgres",password="",host="127.0.0.1",port="5432")
    cur = conn.cursor()
    change_id_card = '\'' + id_card + '\''
    change_name = '\'' + name + '\''
    change_sex = '\'' + sex + '\''
    change_tele = '\'' + tele + '\''
    change_situ = '\'' + situ + '\''
    sql= 'insert into people values (' + change_id_card + ',' + change_name + ',' + change_sex + ',' + change_tele + ',' + change_situ + ')'
    print(sql)
    cur.execute(sql)
    conn.commit()
    print('插入成功')

def delete(input_id_card):
    conn = psycopg2.connect(database="vaccine_ms",user="postgres",password="",host="127.0.0.1",port="5432")
    cur = conn.cursor()
    change_id = '\'' + input_id_card + '\''
    sql = 'delete from people where id_card = ' + change_id
    print(sql)
    cur.execute(sql)
    conn.commit()
    print('删除成功')

def select(input_id_card, input_name):
    conn = psycopg2.connect(database="vaccine_ms",user="postgres",password="",host="127.0.0.1",port="5432")
    cur = conn.cursor()
    change_id = '\'' + input_id_card + '\''
    change_name = '\'' + input_name + '\''
    sql = 'select * from people where id_card = ' + change_id + ' AND ' + 'name = ' + change_name
    print(sql)
    cur.execute(sql)
    conn.commit()
    # cur.fetchall()获取查询结果
    get_data = cur.fetchall()
    return get_data
def change_data(id_card, name, sex, tele, situ):
    conn = psycopg2.connect(database="vaccine_ms", user="postgres", password="", host="127.0.0.1", port="5432")
    cur = conn.cursor()
    change_id_card = '\'' + id_card + '\''
    sql = 'delete from people where id_card = ' + change_id_card
    cur.execute(sql)
    conn.commit()
    change_name = '\'' + name + '\''
    change_sex = '\'' + sex + '\''
    change_tele = '\'' + tele + '\''
    change_situ = '\'' + situ + '\''
    sql = 'insert into people values (' + change_id_card + ',' + change_name + ',' + change_sex + ',' + change_tele + ',' + change_situ + ')'
    cur.execute(sql)
    conn.commit()