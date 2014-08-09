'''
Created on 2013-6-4

@author: YUWANG
'''

from db.models import *
from django.db import connection


def list_transactionBill():
    return transactionBill.objects.all()


def get_searchConditions(formValue):
    conditionDict = {}

    conditionDict['itemType'] = formValue.POST['itemType']
    conditionDict['account'] = formValue.POST['account']
    conditionDict['customer'] = formValue.POST['customer']
    conditionDict['year'] = formValue.POST['year']
    conditionDict['month'] = formValue.POST['month']

    return conditionDict


def get_transactions(paraInfo):
    return transactionBill.objects.filter(**paraInfo)


def search_account(account, year, month):
    searchSql = "select c.name,a.id,sum(t.deposit),sum(t.expense) from customer c,account a,transactionBill t where a.id=%s"
    variableStr = []
    variableStr.append(account)

    if year:
        searchSql += " and year(t.transactionDate)=%s "
        variableStr.append(year)

    if month:
        searchSql += " and month(t.transactionDate)=%s "
        variableStr.append(month)

    searchSql += " and a.customerId=c.id and a.id=t.accountId"

    # statistics
    cursor = connection.cursor()
    cursor.execute(searchSql, variableStr)
    accounts = cursor.fetchall()

    return accounts


def search_customer(customer, year, month):
    searchSql = "select a.id,sum(t.deposit),sum(t.expense) from customer c,account a,transactionBill t where c.name=%s"
    variableStr = []
    variableStr.append(customer)

    if year:
        searchSql += " and year(t.transactionDate)=%s "
        variableStr.append(year)

    if month:
        searchSql += " and month(t.transactionDate)=%s "
        variableStr.append(month)

    searchSql += " and a.customerId=c.id and a.id=t.accountId group by a.id"

    # statistics
    cursor = connection.cursor()
    num = cursor.execute(searchSql, variableStr)
    accounts = cursor.fetchall()

    return accounts
