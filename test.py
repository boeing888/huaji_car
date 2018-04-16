#! /usr/bin/env python3
# -*- coding:utf-8 -*-

import pymysql

if __name__ == '__main__':
    conn=pymysql.connect(host="localhost", user="root",password="Aa111111", db="real_estate", port=3306, charset='utf8mb4')
    cur = conn.cursor()
    cur.callproc('select_view_car_sold1',('test03',))
    a=cur.fetchall()
    cur.callproc('select_view_car_sold0',('test03',))
    b=cur.fetchall()
    print(a)
    print(b)
    print(a+b)