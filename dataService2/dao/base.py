# coding=utf-8
# import os
# import sys
# sys.path.append(os.getcwd() + '/../')
import MySQLdb
from django.db import connection
from django.db import transaction
import json
from log import logto
import time
import logging

def get_cursor1():
    db = MySQLdb.connect(host='192.168.0.213', port='3306', user='root', passwd='abc123', db='dataServiceDB')
    return db.cursor()

def get_cursor():
    return connection.cursor()

def check_regist_loginName(loginName):
    cursor = get_cursor()
    cursor.execute('select id from t_account where loginName=\'' + loginName + '\'')
    res = cursor.fetchall()
    return res

def check_regist_email(email):
    cursor = get_cursor()
    sql = 'select id from t_account where email=\'' + email + '\''
    cursor.execute(sql)
    res = cursor.fetchall()
    return res

def get_account(loginName, loginPass):
    sql = '''select loginName from t_account 
    where loginName='%s' and loginPassword=MD5(MD5('%s'))''' % (loginName, loginPass)
    cursor = get_cursor()
    cursor.execute(sql)
    res = cursor.fetchall()
    return res

def getAccountInfo(loginName):
    sql = '''select id,loginName,email,balance,master,customerID,create_at
    from t_account where loginName='%s' ''' % (loginName)
    cursor = get_cursor()
    cursor.execute(sql)
    res = cursor.fetchall()
    return res

def getMCID(lName):
    sql = '''select master,customerID from t_account where loginName='%s' ''' % (lName)
    cursor = get_cursor()
    cursor.execute(sql)
    res = cursor.fetchall()
    return res

def getCustomerInfo(lName):
    sql = '''select email,name,identification,customerLevel,mobile,address,company,create_at
    from t_customer where id=(select customerID from t_account where loginName='%s') ''' % (lName)
    cursor = get_cursor()
    cursor.execute(sql)
    res = cursor.fetchall()
    return res

def getCustomerInfoByID(id):
    sql = '''select email,name,identification,customerLevel,mobile,address,company,create_at
    from t_customer where id='%s' ''' % (id)
    cursor = get_cursor()
    cursor.execute(sql)
    res = cursor.fetchall()
    return res

def getUserIDByName(loginName):
    cursor = get_cursor()
    sql = '''select id from t_account where loginName='%s' ''' % (loginName)
    cursor.execute(sql)
    res = cursor.fetchall()
    return res[0][0]

def getUserIDInOS(loginName):
    cursor = get_cursor()
    sql = '''select osdb_user from t_account where loginName='%s' ''' % (loginName)
    cursor.execute(sql)
    res = cursor.fetchall()
    return res[0][0]

def getUserIDInOSByID(user_id):
    cursor = get_cursor()
    sql = '''select osdb_user from t_account where t_account.id=%d ''' % (user_id)
    cursor.execute(sql)
    res = cursor.fetchall()
    return res[0][0]

def getUserOSIDByName(user_loginName):
    cursor = get_cursor()
    sql = '''select osdb_user from t_account where t_account.loginName='%s' ''' % (user_loginName)
    cursor.execute(sql)
    res = cursor.fetchall()
    return res[0][0]

# v2.2, in use
def getTenantIDByName(tenantName):
    cursor = get_cursor()
    sql = '''select id from t_tenant where t_tenant.name='%s' ''' % (tenantName)
    cursor.execute(sql)
    res = cursor.fetchall()
    return res[0][0]

# v2.2, in use
def getTenantOSIDByName(tenantName):
    cursor = get_cursor()
    sql = '''select t_tenant.osdb_tenant from t_tenant where t_tenant.name='%s' ''' % (tenantName)
    cursor.execute(sql)
    res = cursor.fetchall()
    try:
        return res[0][0]
    except:
        return ''

# v2.2, in use
def getRoleIDByName(roleName):
    cursor = get_cursor()
    sql = '''select id from t_role where t_role.name='%s' ''' % (roleName)
    cursor.execute(sql)
    res = cursor.fetchall()
    return res[0][0]

# v2.2, in use
def getRoleOSIDByName(roleName):
    cursor = get_cursor()
    sql = '''select t_role.osdb_role from t_role where t_role.name='%s' ''' % (roleName)
    cursor.execute(sql)
    res = cursor.fetchall()
    return res[0][0]

# v2.2, in use
def getRoleOSIDByID(role_id):
    cursor = get_cursor()
    sql = '''select t_role.osdb_role from t_role where t_role.id=%d ''' % (int(role_id))
    cursor.execute(sql)
    res = cursor.fetchall()
    return res[0][0]

def getUserRoleInTenant(tenant_id):
    cursor = get_cursor()
    sql = '''select t_turMap.id,t_turMap.user,t_turMap.role from t_turMap 
        where t_turMap.delete_at is null and t_turMap.tenant = %d ''' % (tenant_id)
    cursor.execute(sql)
    res = cursor.fetchall()
    return res

# v2.2, in use, many functions
def getMasterOfAccount(loginName):
    cursor = get_cursor()
    sql = '''select master from t_account where loginName='%s' ''' % (loginName)
    cursor.execute(sql)
    res = cursor.fetchall()
    return res[0][0]

def getSubAccountList(master):
    cursor = get_cursor()
    sql = '''select loginName,email,balance,master,customerID,create_at 
    from t_account where delete_at is NULL and master='%s' ''' % (master)
    cursor.execute(sql)
    res = cursor.fetchall()
    acc_list = []
    for i in range(len(res)):
        acc = {
               'loginName':res[i][0],
               'email':res[i][1],
               'balance':res[i][2],
               'master':res[i][3],
               'customerID':res[i][4],
               'create_at':res[i][5],
               }
        acc_list.append(acc)
    return acc_list

def getUserListOfOwner(name):
    sql = '''select loginName,osdb_user,email,balance,master,customerID,create_at 
        from t_account where delete_at is NULL and (master='%s' or loginName='%s') ''' % (
        name, name)
    cursor = get_cursor()
    cursor.execute(sql)
    res = cursor.fetchall()
    user_list = []
    for i in range(len(res)):
        acc = {
               'loginName':res[i][0],
               'osid':res[i][1],
               'email':res[i][2],
               'balance':res[i][3],
               'master':res[i][4],
               'customerID':res[i][5],
               'create_at':res[i][6],
               }
        user_list.append(acc)
    return user_list

# v2.2, in use
def check_tenant_create_name(tenant_name):
    cursor = get_cursor()
    sql = '''select count(*) from t_tenant where name='%s' ''' % (tenant_name)
    cursor.execute(sql)
    res = cursor.fetchall()
    return res[0][0]

# v2.2, in use
def check_user_create_name(user_name):
    cursor = get_cursor()
    sql = '''select count(*) from t_account where loginName='%s' ''' % (user_name)
    cursor.execute(sql)
    res = cursor.fetchall()
    return res[0][0]

# v2.2, in use
def getSysRoleList():
    sql = '''select id,osdb_role,name 
        from t_role
        where delete_at is NULL '''
    cursor = get_cursor()
    cursor.execute(sql)
    res = cursor.fetchall()
    sys_role_list = []
    for i in range(len(res)):
        if(res[i][0] != 1 and res[i][0] != 2):
            s_r = {
                 'id':res[i][0],
                 'osid':res[i][1],
                 'name':res[i][2],
                 }
            sys_role_list.append(s_r)
    return sys_role_list

def getDataProcessingIDByName(dp_name):
    cursor = get_cursor()
    sql = '''select id from t_dataProcessing where processName='%s' ''' % (dp_name)
    cursor.execute(sql)
    res = cursor.fetchall()
    return res[0][0]

def getDataProcessingServerNameByID(dpid):
    cursor = get_cursor()
    sql = '''select serverName from t_dataProcessing where id='%d' ''' % (dpid)
    cursor.execute(sql)
    res = cursor.fetchall()
    return res[0][0]

def getDataProcessingServers(dpid):
    cursor = get_cursor()
    sql = '''SELECT t_dpMes.metadata 
            FROM t_dpMes 
            WHERE t_dpMes.dpid=%d 
            and t_dpMes.message='serverStatus' ''' % (dpid)
    cursor.execute(sql)
    res = cursor.fetchall()
    resList = list(res)
    return resList

def getDataProcessingMes(dpid):
    cursor = get_cursor()
    sql = '''SELECT id,time,message,metadata 
            FROM t_dpMes 
            WHERE dpid=%d 
            ORDER BY id 
            DESC LIMIT 0 ,10''' % (dpid)
    cursor.execute(sql)
    res = cursor.fetchall()
    resList = []
    for r in res:
        dic = {
             'id':r[0],
             'time':r[1],
             'message':r[2],
             'metadata':r[3]
             }
        resList.append(dic)
    return resList
