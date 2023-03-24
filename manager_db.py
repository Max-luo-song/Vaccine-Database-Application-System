#encoding: utf-8
'''
    操作manager表，涉及操作为查询
'''
import psycopg2

def select(input_id, input_password):
    conn = psycopg2.connect(database="vaccine_ms",user="postgres",password="",host="127.0.0.1",port="5432")
    cur = conn.cursor()
    change_id = '\'' + input_id + '\''
    change_password = '\'' + input_password + '\''
    sql = 'select * from manager where id = ' + change_id + ' AND ' + 'password = ' + change_password
    print(sql)
    cur.execute(sql)
    conn.commit()
    # cur.fetchall()获取查询结果
    get_data = cur.fetchall()
    return get_data