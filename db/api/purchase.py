'''
Created on 2013-6-4

@author: YUWANG
'''
from django.db import connection
from db.models import purchaseProduct, purchasePackage


def list_purchaseProducts():
    cursor = connection.cursor()
    cursor.execute(""" select transactionId,transactionDate,c.name,p.name, pp.discountValue,duration,quantity,pp.comment from purchaseProduct pp,product p,customer c where pp.customerId=c.id and pp.productId=p.id """)
    purchaseProducts = cursor.fetchall()
    return purchaseProducts


def list_purchasePackages():
    cursor = connection.cursor()
    cursor.execute(""" select transactionId,transactionDate,c.name,p.name,duration,quantity,pp.comment from purchasePackage pp,package p,customer c where pp.customerId=c.id and pp.packageId=p.id """)
    purchasePackages = cursor.fetchall()
    return purchasePackages


def get_searchConditions(formValue):
    conditionDict = {}
    conditionDict['productType'] = formValue.POST['productType']
    conditionDict['customer'] = formValue.POST['customer']
    conditionDict['service'] = formValue.POST['service']
    conditionDict['year'] = formValue.POST['year']
    conditionDict['month'] = formValue.POST['month']

    return conditionDict


def search_purchaseProducts(conditionValue):
    searchProductSql = "select transactionId,transactionDate,c.name,p.name,pp.discountValue,duration,quantity,pp.comment from product p,customer c,purchaseProduct pp where "
    searchSql = get_sql(conditionValue)
    searchProductSql = searchProductSql+searchSql+" pp.customerId=c.id and pp.productId=p.id"
    searchVariable = get_variable(conditionValue)
    cursor = connection.cursor()
    cursor.execute(searchProductSql, searchVariable)
    products = cursor.fetchall()

    return products


def search_purchasePackages(conditionValue):
    searchPackageSql = "select transactionId,transactionDate,c.name,p.name,duration,quantity,pp.comment from package p,customer c,purchasePackage pp where "
    searchSql = get_sql(conditionValue)
    searchPackageSql = searchPackageSql+searchSql+" pp.customerId=c.id and pp.packageId=p.id"
    searchVariable = get_variable(conditionValue)
    cursor = connection.cursor()
    cursor.execute(searchPackageSql, searchVariable)
    packages = cursor.fetchall()

    return packages


def get_sql(formValue):
    searchSql = ""

    if formValue['customer']:
        searchSql += "c.name=%s and "

    if formValue['service']:
        searchSql += "p.name=%s and"

    if formValue['year']:
        searchSql += "year(transactionDate)=%s and "

    if formValue['month']:
        searchSql += "month(transactionDate)=%s and "

    return searchSql


def get_variable(formValue):
    variableStr = []

    if formValue['customer']:
        variableStr.append(formValue['customer'])

    if formValue['service']:
        variableStr.append(formValue['service'])

    if formValue['year']:
        variableStr.append(formValue['year'])

    if formValue['month']:
        variableStr.append(formValue['month'])

    return variableStr
