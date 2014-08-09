# coding=utf-8
from django.shortcuts import render_to_response
from django.http import HttpResponse
import MySQLdb
from django.db import connection

def testapp(request):
#    db = MySQLdb.connect(user='me', db='mydb', passwd='secret', host='localhost')
#    cursor = db.cursor()
    connection.queries
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM account')
    accounts = cursor.fetchall()
    p1 = {'SN':'0a', 'LoginName':'abc', 'LoginPass':'def', 'User':'no name', 'Status':1}
    p2 = {'SN':11, 'LoginName':'abc', 'LoginPass':'def', 'User':'no name', 'Status':1} 
    accList = [p1, p2, ]
    for i in range(len(accounts)):
        new = {
             'SN':accounts[i][0],
             'LoginName':accounts[i][1],
             'LoginPass':accounts[i][2],
             'User':accounts[i][3],
             'Status':accounts[i][4]
            }
        accList.append(new)
    return render_to_response('hello/hello5.html', locals())
#
#
#
#
#
