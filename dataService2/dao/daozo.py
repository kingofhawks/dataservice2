# coding=utf-8
# import os
# import sys
# sys.path.append(os.getcwd() + '/../')
import MySQLdb
from django.db import connection
from django.db import transaction
from log import logto
from osao import keystone
# from bean import customer
import time
import logging
import base

##### ###### for default ##### ###### ##### ###### ##### ###### ##### ######

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

@transaction.commit_manually
def account_regist(name, password, email):
    cursor = get_cursor()
    uuid = ''
    try:
        uuid = keystone.user_create(name, password, email)
        if(uuid == 'ERROR'):
            return False
        else:
            sql = '''insert into t_account values (null,'%s','%s',MD5(MD5('%s')),'%s',0,null,null,'%s',null) ''' % (
            uuid, name, password, email, time.strftime('%Y-%m-%d %X', time.localtime()))
            cursor.execute(sql)
    except:
        logging.getLogger('operate').log(30, 'add customer %s %s %s failed.' % 
        (name, password, email))
        keystone.user_delete(uuid)
        transaction.rollback()
        flag = False
    else:
        logging.getLogger('operate').log(20, 'add customer %s %s %s successed.' % 
        (name, password, email))
        transaction.commit()
        flag = True
    finally:
        pass
        # print "Arrive finally"
    return flag

def get_account(loginName, loginPass):
    sql = '''select loginName,id from t_account 
    where loginName='%s' and loginPassword=MD5(MD5('%s'))''' % (loginName, loginPass)
    cursor = get_cursor()
    cursor.execute(sql)
    res = cursor.fetchall()
    return res

##### ###### end for other ##### ###### ##### ###### ##### ###### ##### ######

##### ###### for my app ##### ###### ##### ###### ##### ###### ##### ######

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

def getAllOfOne(loginName):
    sql = '''select customerName,customerBalance from t_customer where loginName='%s' ''' % (loginName)
    cursor = get_cursor()
    cursor.execute(sql)
    res = cursor.fetchall()
    return res

def getUserID(loginName):
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

def getTenantID(tenantName):
    cursor = get_cursor()
    sql = '''select id from t_tenant where t_tenant.name='%s' ''' % (tenantName)
    cursor.execute(sql)
    res = cursor.fetchall()
    return res[0][0]

def getTenantOSID(tenantName):
    cursor = get_cursor()
    sql = '''select t_tenant.osdb_tenant from t_tenant where t_tenant.name='%s' ''' % (tenantName)
    cursor.execute(sql)
    res = cursor.fetchall()
    return res[0][0]

def getRoleID(roleName):
    cursor = get_cursor()
    sql = '''select id from t_role where t_role.name='%s' ''' % (roleName)
    cursor.execute(sql)
    res = cursor.fetchall()
    return res[0][0]

def getRoleIDInOS(roleName):
    cursor = get_cursor()
    sql = '''select t_role.osdb_role from t_role where t_role.name='%s' ''' % (roleName)
    cursor.execute(sql)
    res = cursor.fetchall()
    return res[0][0]

def getRoleIDInOSByID(role_id):
    cursor = get_cursor()
    sql = '''select t_role.osdb_role from t_role where t_role.id=%d ''' % (role_id)
    cursor.execute(sql)
    res = cursor.fetchall()
    return res[0][0]

def getTenantList(loginName):
    sql = '''select t_tenant.name,t_role.name,t_tenant.create_at,t_tenant.description
    from t_turMap,t_tenant,t_account,t_role
    where t_turMap.delete_at is null 
    and t_turMap.tenant=t_tenant.id 
    and t_turMap.user=t_account.id 
    and t_turMap.role=t_role.id 
    and t_account.loginName='%s'  ''' % (loginName)
    cursor = get_cursor()
    cursor.execute(sql)
    res = cursor.fetchall()
    return res

# v2.2, in use, tenant_detail
def getTenantDetail(tenant_id):
    sql = ''' select t_tenant.name,t_tenant.description,t_tenant.create_at,
    t_account.loginName,t_tenant.id,t_tenant.osdb_tenant
    from t_tenant,t_account
    where t_tenant.delete_at is null
    and t_tenant.create_by=t_account.id
    and t_tenant.name = '%s' ''' % (tenant_id)
    cursor = get_cursor()
    cursor.execute(sql)
    res = cursor.fetchall()
    if(len(res) == 1):
        tenant = {
                'name':res[0][0],
                'desc':res[0][1],
                'create_at':res[0][2],
                'owner':res[0][3],
                'id':res[0][4],
                'osid':res[0][5],
                }
    else:
        tenant = None
    return tenant

# v2.2, in use, tenant_detail
def getTenantUserList(tenant_id):
    sql = '''select t_account.loginName,t_role.name,t_turMap.create_at ,t_turMap.description 
        from t_turMap,t_tenant,t_account,t_role 
        where t_turMap.delete_at is NULL
        and t_turMap.tenant=t_tenant.id 
        and t_turMap.user=t_account.id 
        and t_turMap.role=t_role.id  
        and t_tenant.id=%d ''' % (tenant_id)
    cursor = get_cursor()
    cursor.execute(sql)
    res = cursor.fetchall()
    if(len(res) > 0):
        user_list = []
        for i in range(len(res)):
            u = {
               'name':res[i][0],
               'role':res[i][1],
               'create_at':res[i][2],
               'desc':res[i][3],
               }
            user_list.append(u)
    else:
        user_list = None
    return user_list

# v2.2, in use, user_detail
def getUserDetail(name):
    sql = '''SELECT id,osdb_user,loginName,email,balance,customerID,create_at,master
        from t_account
        where delete_at is NULL
        and t_account.loginName='%s' ''' % (name)
    cursor = get_cursor()
    cursor.execute(sql)
    res = cursor.fetchall()
    if(len(res) == 1):
        user = {
                'id':res[0][0],
                'osid':res[0][1],
                'loginName':res[0][2],
                'email':res[0][3],
                'balance':res[0][4],
                'customerID':res[0][5],
                'create_at':res[0][6],
                'master':res[0][7],
              }
    else:
        user = None
    return user

def getUserRoleInTenant(tenant_id):
    cursor = get_cursor()
    sql = '''select t_turMap.id,t_turMap.user,t_turMap.role from t_turMap 
        where t_turMap.delete_at is null and t_turMap.tenant = %d ''' % (tenant_id)
    cursor.execute(sql)
    res = cursor.fetchall()
    return res

# v2.2, in use, user_list, user_detail
def getUser_TenantRole(name):
    sql = '''select t_account.loginName,t_tenant.name,t_role.name,t_turMap.create_at,t_turMap.description
        from t_turMap,t_tenant,t_account,t_role 
        where t_turMap.delete_at is NULL 
        and t_turMap.tenant=t_tenant.id 
        and t_turMap.user=t_account.id 
        and t_turMap.role=t_role.id 
        and t_account.loginName='%s' ''' % (name)
    cursor = get_cursor()
    cursor.execute(sql)
    res = cursor.fetchall()
    if(len(res) > 0):
        u_tr_list = []
        for i in range(len(res)):
            u_tr = {
                    'name':res[i][0],
                    'tenant':res[i][1],
                    'role':res[i][2],
                    'create_at':res[i][3],
                    'desc':res[i][4],
                  }
            u_tr_list.append(u_tr)
    else:
        u_tr_list = None
    return u_tr_list

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

@transaction.commit_manually
def customer_add(lName, name, idNo, email, mobile, company, address):
    cursor = get_cursor()
    sql = '''insert into t_customer (id,email,name,identification,customerLevel,mobile,address,company,create_at) 
            values (null,'%s','%s','%s',1,'%s','%s','%s','%s') ''' % (
            email, name, idNo, mobile, address, company, time.strftime('%Y-%m-%d %X', time.localtime()))
    if(cursor.execute(sql) == 1):
        logging.getLogger('operate').log(20, 'customer add %s %s successed.' % (name, idNo))
        sql2 = '''update t_account set t_account.customerID=
        (select id from t_customer where t_customer.identification='%s') 
        where t_account.loginName='%s' ''' % (idNo, lName)
        if(cursor.execute(sql2) == 1):
            logging.getLogger('operate').log(20, 'account update %s %s successed.' % (lName, idNo))
            transaction.commit()
            flag = True
        else:
            logging.getLogger('operate').log(30, 'account update %s %s failed.' % (lName, idNo))
            transaction.rollback()
            flag = False
    else:
        logging.getLogger('operate').log(30, 'customer add %s %s failed.' % (name, idNo))
        transaction.rollback()
        flag = False
    return flag


@transaction.commit_on_success
def tenant_create2(owner_loginName, tenant_name, tenant_desc):
   cursor = get_cursor()
   uuid = ''
   flag = False
   try:
       tenant = keystone.tenant_create(tenant_name, tenant_desc)
       uuid = keystone.get_baseID(tenant)
       res = keystone.add_tenant_user_role(uuid, str(getUserIDInOS(owner_loginName)), str(getRoleIDInOS('owner')))
   except:
       logging.getLogger('operate').log(30, 'tenant create %s %s %s keystone failed.' % (owner_loginName, tenant_name, tenant_desc))
       keystone.remove_tenant_user_role(uuid, str(getUserIDInOS(owner_loginName)), str(getRoleIDInOS('owner')))
       keystone.tenant_delete(uuid)
   else:
       try:
           sql = '''insert into t_tenant values (null,'%s','%s','%s',%d,'%s',null) ''' % (
                   uuid, tenant_name, tenant_desc, getUserID(owner_loginName),
                   time.strftime('%Y-%m-%d %X', time.localtime()))
           cursor.execute(sql)
           sql2 = '''insert into t_turMap values (null,%d,%d,%d,'%s','%s',null) ''' % (
                   getTenantID(tenant_name), getUserID(owner_loginName), getRoleID('owner'),
                   tenant_desc, time.strftime('%Y-%m-%d %X', time.localtime()))
           cursor.execute(sql2)
       except:
           logging.getLogger('operate').log(30, 'tenant create %s %s %s sql failed.' % (
                   owner_loginName, tenant_name, tenant_desc))
           flag = False
           # transcation.rollback()
       else:
           logging.getLogger('operate').log(20, 'tenant create %s %s %s successed.' % (
                   owner_loginName, tenant_name, tenant_desc))
           flag = True
           # transcation.commit()
       finally:
           pass
   finally:
       pass
   return flag

# depreacted
# @transaction.commit_manually
# def tenant_create(owner_loginName, tenant_name, tenant_desc):  # instead by tenant_create2
#    cursor = get_cursor()
#    uuid = ''
#    flag = False
#    # print '''get tenant : %s,%s,%s ''' % (owner_loginName, tenant_name, tenant_desc)
#    uuid = keystone.tenant_create(tenant_name, tenant_desc)
#    # print 'get id of tenant from keystone ,id: ' + uuid
#    if(uuid == 'ERROR'):
#        # print 'uuid error'
#        flag = False
#    else:
#        # print 'uuid right'
#        try:
#            # print 'prepaer sql '
#            sql = ''' insert into t_tenant values (null,'%s','%s','%s','%s','%s',null) ''' % (
#            uuid, tenant_name, tenant_desc, str(getUserID(owner_loginName)),
#            time.strftime('%Y-%m-%d %X', time.localtime()))
#            # print 't_tenant: ' + sql
#            cursor.execute(sql)
#            # print 'prepaer sql2 '
#            # print str(getRoleID('owner'))
#            # print str(getTenantID(tenant_name))
#            sql2 = ''' insert into t_turMap values (null,%s,%s,%s,'%s','%s',null) ''' % (
#            str(getTenantID(tenant_name)), str(getUserID(owner_loginName)), str(getRoleID('owner')),
#            tenant_desc, time.strftime('%Y-%m-%d %X', time.localtime()))
#            # print 't_turmap: ' + sql2
#            cursor.execute(sql2)
#            keystone.add_tenant_user_role(uuid, str(getUserIDInOS(owner_loginName)), str(getRoleID('owner')))
#        except:
#            logging.getLogger('operate').log(30, 'tenant create %s %s %s failed.' % 
#            (owner_loginName, tenant_name, tenant_desc))
#            keystone.tenant_delete(uuid)
#            keystone.remove_tenant_user_role(uuid, str(getUserIDInOS(owner_loginName)), str(getRoleID('owner')))
#            # print "tenant create execute rollback "
#            flag = False
#            transaction.rollback()
#        else:
#            logging.getLogger('operate').log(20, 'tenant create %s %s %s successed.' % 
#            (owner_loginName, tenant_name, tenant_desc))
#            # print "tenant create execute commit "
#            flag = True
#            transaction.commit()
#        finally:
#            pass
#            # print "tenant create execute finally"
#    return flag

@transaction.commit_on_success
def tenant_delete(tenant_name):
    flag = False
    uuid = None
    try:
        tenant_id = getTenantID(tenant_name)
        tenant_uuid = getTenantOSID(tenant_name)
        userRole = getUserRoleInTenant(tenant_id)
        # print userRole
        id_list = ''
        for i in range(len(userRole)):
            id_list = id_list + str(userRole[i][0]) + ','
            # print 'enter remove_tenant_user_role'
            keystone.remove_tenant_user_role(tenant_uuid, str(getUserIDInOSByID(userRole[i][1])),
                str(getRoleIDInOSByID(userRole[i][2])))
        # print 'enter tenant_delete'
        keystone.tenant_delete(tenant_uuid)
    except:
        logging.getLogger('operate').log(30, 'DAOZO tenant delete %s %s %s failed.' % (
            tenant_name, id, uuid))
        flag = False
    else:
        try:
            cursor = get_cursor()
            sql1 = '''update t_turMap set delete_at = '%s' where t_turMap.id in (%s) ''' % (
                time.strftime('%Y-%m-%d %X', time.localtime()), id_list[:-1])
            # print sql1
            sql2 = '''update t_tenant set delete_at = '%s' where t_tenant.id=%s ''' % (
                time.strftime('%Y-%m-%d %X', time.localtime()), tenant_id)
            # print sql2
            cursor.execute(sql1)
            cursor.execute(sql2)
        except:
            logging.getLogger('operate').log(30, 'DAOZO tenant delete %s %s %s failed.' % (
                tenant_name, id, uuid))
            flag = False
        else:
            logging.getLogger('operate').log(20, 'DAOZO tenant delete %s %s %s successful.' % (
                tenant_name, id, uuid))
            flag = True
        finally:
            pass
    finally:
        pass
    return flag

@transaction.commit_manually
def sub_account_create(loginName, name, password, email):
    cursor = get_cursor()
    uuid = ''
    try:
        uuid = keystone.user_create(name, password, email)
        if(uuid == 'ERROR'):
            return False
        else:
            sql = '''insert into t_account values (null,'%s','%s',MD5(MD5('%s')),'%s',0,'%s',null,'%s',null) ''' % (
            uuid, name, password, email, loginName, time.strftime('%Y-%m-%d %X', time.localtime()))
            cursor.execute(sql)
    except:
        logging.getLogger('operate').log(30, 'create sub-account failed %s %s %s %s .' % 
        (loginName, name, password, email))
        keystone.user_delete(uuid)
        transaction.rollback()
        flag = False
    else:
        logging.getLogger('operate').log(20, 'create sub-account successed %s %s %s %s.' % 
        (loginName, name, password, email))
        transaction.commit()
        flag = True
    finally:
        pass
        # print "Arrive finally"
    return flag

@transaction.commit_on_success
def sub_account_delete(name):
    try:
        keystone.user_delete(getUserIDInOS(name))
    except:
        logging.getLogger('operate').log(30, 'DAOZO sub_account delete %s failed.' % (name))
        flag = False
    else:
        try:
            cursor = get_cursor()
            sql = '''update t_account set delete_at = '%s' where t_account.loginName='%s' ''' % (
                time.strftime('%Y-%m-%d %X', time.localtime()), name)
            cursor.execute(sql)
        except:
            logging.getLogger('operate').log(30, 'DAOZO sub_account delete %s failed.' % (name))
            flag = False
        else:
            logging.getLogger('operate').log(20, 'DAOZO sub_account delete %s successful.' % (name))
            flag = True
    finally:
        return flag

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

# v2.2, in use
@transaction.commit_on_success
def tenant_add_user(tenant, user, role):
    # print tenant
    # print base.getTenantIDByName(tenant)
    # print base.getTenantOSIDByName(tenant)
    # print user
    # print base.getUserIDByName(user)
    # print base.getUserOSIDByName(user)
    # print role
    # print base.getRoleOSIDByID(role)
    flag = False
    try:
        res = keystone.add_tenant_user_role(str(base.getTenantOSIDByName(tenant)),
            str(base.getUserOSIDByName(user)), str(base.getRoleOSIDByID(role)))
    except:
        print 'keystone tenant add user failed.'
    else:
        flag = True
        print 'keystone tenant add user successful.'
        try:
            cursor = base.get_cursor()
            sql = '''INSERT into t_turMap VALUES (NULL,%d,%d,%d,NULL,'%s',NULL)''' % (
                    int(base.getTenantIDByName(tenant)), int(base.getUserIDByName(user)), int(role),
                    time.strftime('%Y-%m-%d %X', time.localtime()))
            print sql
            cursor.execute(sql)
        except:
            print 'sql tenant add user failed.'
            flag = False
        else:
            print 'sql tenant add user successful.'
            flag = True
    finally:
        return flag


# v2.2, in use
@transaction.commit_on_success
def tenant_del_user(tenant, user, role):
    # print tenant
    # print base.getTenantIDByName(tenant)
    # print base.getTenantOSIDByName(tenant)
    # print user
    # print base.getUserIDByName(user)
    # print base.getUserOSIDByName(user)
    # print role
    # print base.getRoleOSIDByID(role)
    flag = False
    try:
        res = keystone.remove_tenant_user_role(str(base.getTenantOSIDByName(tenant)),
            str(base.getUserOSIDByName(user)), str(base.getRoleOSIDByName(role)))
    except:
        print 'keystone tenant del user failed.'
    else:
        flag = True
        print 'keystone tenant del user successful.'
        try:
            cursor = base.get_cursor()
            sql = '''UPDATE t_turMap set delete_at='%s'
                where tenant=%d 
                and user=%d 
                and role=%d 
                and delete_at is NULL ''' % (time.strftime('%Y-%m-%d %X', time.localtime()),
                    int(base.getTenantIDByName(tenant)), int(base.getUserIDByName(user)), int(base.getRoleIDByName(role)))
            print sql
            cursor.execute(sql)
        except:
            print 'sql tenant del user failed.'
            flag = False
        else:
            print 'sql tenant del user successful.'
            flag = True
    finally:
        return flag

# v2.2, in use
def getTenantCountOfUser(user_name):
    sql = '''select count(*) from t_turMap 
        where t_turMap.user = %d and t_turMap.delete_at is NULL''' % (base.getUserIDByName(user_name))
    cursor = base.get_cursor()
    cursor.execute(sql)
    res = cursor.fetchall()
    return res[0][0]

# v2.2, in use
def getUserCountOfTenant(tenant_name):
    sql = '''select count(*) from t_turMap 
        where t_turMap.tenant = %d 
        and t_turMap.role != 2
        and t_turMap.delete_at is NULL''' % (base.getTenantIDByName(tenant_name))
    cursor = base.get_cursor()
    cursor.execute(sql)
    res = cursor.fetchall()
    return res[0][0]

##### ##### end for my app ##### ###### ##### ###### ##### ###### ##### ######

##### ##### for dp app     ##### ###### ##### ###### ##### ###### ##### ######

def data_processing_list(tenant):
    sql = '''SELECT processName,t_tenant.name,t_account.loginName,
        algofile,datafile,output,serverName,serverCount,
        t_dataProcessing.create_at,end_at,status,t_dataProcessing.id 
        FROM t_dataProcessing,t_account,t_tenant 
        WHERE t_dataProcessing.tenant=t_tenant.id 
        AND t_dataProcessing.user=t_account.id 
        AND t_tenant.delete_at IS NULL 
        AND t_tenant.name='%s'
        ''' % (tenant)
    cursor = get_cursor()
    dpList = []
    if(cursor.execute(sql) > 0):
        res = cursor.fetchall()
        for dp in res:
            dp = {
                'name':dp[0],
                'tenant':dp[1],
                'user':dp[2],
                'algofile':dp[3],
                'datafile':dp[4],
                'output':dp[5],
                'serverName':dp[6],
                'serverCount':dp[7],
                'create_at':dp[8],
                'end_at':dp[9],
                'status':dp[10],
                'id':dp[11],
                }
            dpList.append(dp)
    else:
        dpList = []
    return dpList

def data_processing_detailByName(dp_name):
    sql = '''SELECT processName,t_tenant.name,t_account.loginName,
        algofile,datafile,output,serverName,serverCount,
        t_dataProcessing.create_at,end_at,status,t_dataProcessing.id,
        serverConfig, serverMeta,hadoopMeta
        FROM t_dataProcessing,t_account,t_tenant 
        WHERE t_dataProcessing.tenant=t_tenant.id 
        AND t_dataProcessing.user=t_account.id 
        AND t_tenant.delete_at IS NULL 
        AND t_dataProcessing.processName='%s'
        ''' % (dp_name)
    cursor = get_cursor()
    detail = {}
    if(cursor.execute(sql) == 1):
        res = cursor.fetchall()
        detail = {
                'name':res[0][0],
                'tenant':res[0][1],
                'user':res[0][2],
                'algofile':res[0][3],
                'datafile':res[0][4],
                'output':res[0][5],
                'serverName':res[0][6],
                'serverCount':res[0][7],
                'create_at':res[0][8],
                'end_at':res[0][9],
                'status':res[0][10],
                'id':res[0][11],
                'serverConfig':res[0][12],
                'serverMeta':res[0][13],
                'hadoopMeta':res[0][14],
                }
    else:
        detail = {}
    return detail

def data_processing_detail(id):
    sql = '''SELECT processName,t_tenant.name,t_account.loginName,
        algofile,datafile,output,serverName,serverCount,
        t_dataProcessing.create_at,end_at,status,t_dataProcessing.id,
        serverConfig, serverMeta,hadoopMeta
        FROM t_dataProcessing,t_account,t_tenant 
        WHERE t_dataProcessing.tenant=t_tenant.id 
        AND t_dataProcessing.user=t_account.id 
        AND t_tenant.delete_at IS NULL 
        AND t_dataProcessing.id=%d
        ''' % (int(id))
    cursor = get_cursor()
    detail = {}
    if(cursor.execute(sql) == 1):
        res = cursor.fetchall()
        detail = {
                'name':res[0][0],
                'tenant':res[0][1],
                'user':res[0][2],
                'algofile':res[0][3],
                'datafile':res[0][4],
                'output':res[0][5],
                'serverName':res[0][6],
                'serverCount':res[0][7],
                'create_at':res[0][8],
                'end_at':res[0][9],
                'status':res[0][10],
                'id':res[0][11],
                'serverConfig':res[0][12],
                'serverMeta':res[0][13],
                'hadoopMeta':res[0][14],
                }
    else:
        detail = {}
    return detail

@transaction.commit_on_success
def data_processing_launch(dp_name, tenant, user, algoFile, dataFile, output,
        serverName, serverCount, serverConfig, serverMeta, hadoopMeta):
    sql = '''INSERT INTO t_dataProcessing VALUES (NULL,'%s',
        (SELECT t_tenant.id FROM t_tenant where t_tenant.name = '%s'),
        (SELECT t_account.id FROM t_account where t_account.loginName = '%s'),
        '%s','%s','%s','%s',%d,'%s','%s','%s',
        'building','%s',NULL)
        ''' % (dp_name, tenant, user, algoFile, dataFile, output,
               serverName, serverCount, serverConfig, serverMeta,
               hadoopMeta, time.strftime('%Y-%m-%d %X', time.localtime()))
    #print sql
    cursor = get_cursor()
    if(cursor.execute(sql) == 1):
        logging.getLogger('operate').log(20, 'dataprocessing launch %s successed.' % (dp_name))
        flag = True
    else:
        logging.getLogger('operate').log(30, 'dataprocessing launch %s failed.' % (dp_name))
        flag = False
    return flag

def change():
    print 'change'
##### ##### end for dp app ##### ###### ##### ###### ##### ###### ##### ######
