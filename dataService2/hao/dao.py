import MySQLdb
from django.db import connection
from django.db import transaction
from log import logto
import time
import logging

def get_cursor():
    return connection.cursor()

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
    # print sql
    cursor = get_cursor()
    if(cursor.execute(sql) == 1):
        logging.getLogger('operate').log(20, 'dataprocessing launch %s successed.' % (dp_name))
        flag = True
    else:
        logging.getLogger('operate').log(30, 'dataprocessing launch %s failed.' % (dp_name))
        flag = False
    return flag

@transaction.commit_on_success
def data_process_status_change(dp_id, status):
    sql = '''UPDATE t_dataProcessing SET t_dataProcessing.status='%s' WHERE t_dataProcessing.id=%d
        ''' % (status, int(dp_id))
    cursor = get_cursor()
    if(cursor.execute(sql) == 1):
        flag = True
    else:
        flag = False
    return flag    

@transaction.commit_on_success
def data_process_add_message(dp_id, message, metadata):
    sql = '''INSERT INTO t_dpMes VALUES (NULL,%d,%s,%s,%s);
    ''' % (int(dp_id), time.strftime('%Y-%m-%d %X', time.localtime()), message, metadata)
    cursor = get_cursor()
    if(cursor.execute(sql) == 1):
        flag = True
    else:
        flag = False
    return flag

@transaction.commit_on_success
def data_process_update_status(dp_id, metadata):
    sql = '''UPDATE t_dpMes SET t_dpMes.metadata='%s'
            WHERE t_dpMes.message='serverStatus'
            AND t_dpMes.dpid=%d
            ''' % (metadata, int(dp_id))
    cursor = get_cursor()
    if(cursor.execute(sql) == 1):
        flag = True
    else:
        flag = False
    return flag
