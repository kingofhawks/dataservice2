# coding=utf-8

import MySQLdb
import time
import logging

def get_cursor1():
    db = MySQLdb.connect(host='192.168.0.213', port=3306, user='root', passwd='abc123', db='dataServiceDB')
    return db.cursor()

def getAccountIDByLoignName(loginName):
    cursor = get_cursor1()
    sql = '''select id from t_account where loginName='%s' ''' % (loginName)
    print sql
    cursor.execute(sql)
    print 'loginName:' + loginName
    res = cursor.fetchall()
    print type(res)
    print res
    print type(res[0][0])
    print res[0][0]

if __name__ == "__main__":
    getAccountIDByLoignName('testUser')
