# coding=utf-8
from keystoneclient.v2_0 import client
from keystoneclient.v2_0 import users
from keystoneclient import base
import logging
import datetime
import time

def get_client1():
    TOKEN = 'admin'
    ENDPOINT = 'http://192.168.0.50:35357/v2.0'
    return client.Client(token=TOKEN, endpoint=ENDPOINT)

def get_client4():
    TOKEN = 'admin'
    ENDPOINT = 'http://192.168.0.96:35357/v2.0'
    return client.Client(token=TOKEN, endpoint=ENDPOINT)

def get_client2():
    TOKEN = 'admin'
    ENDPOINT = 'http://192.168.110.120:35357/v2.0'
    return client.Client(token=TOKEN, endpoint=ENDPOINT)

def get_client3():
    USER = 'admin'
    PASS = 'openstack'
    TENANT_NAME = 'adminTenant'
    AUTH_URL = 'http://192.168.0.106:5000/v2.0'
    return client.Client(username=USER, password=PASS, tenant_name=TENANT_NAME, auth_url=AUTH_URL)

def get_baseID(obj):
    return base.getid(obj)

def user_create(name, password, email):
    keystone = get_client1()
    np = ''
    try:
        np = keystone.users.create(name, password, email, None, True)
    except:
        logging.getLogger('operate').log(30, 'KEYSTONE USER_CREATE %s %s %s None True failed.' % 
        (name, password, email))
        return 'ERROR'
    else:
        logging.getLogger('operate').log(20, 'KEYSTONE USER_CREATE  %s %s %s None True success.' % 
        (name, password, email))
        return base.getid(np)

def user_delete(uuid):
    keystone = get_client1()
    res = keystone.users.delete(uuid)
    logging.getLogger('operate').log(20, 'KEYSTONE USER_DELETE %s.' % (uuid))

def tenant_create(tenant_name, tenant_desc):
    nt = None
    try:
        keystone = get_client1()
        nt = keystone.tenants.create(tenant_name, tenant_desc, True)
    except:
        logging.getLogger('operate').log(30, 'KEYSTONE TENANT_CREATE %s %s True failed.' % 
        (tenant_name, tenant_desc))
        return 'ERROR'
    else:
        logging.getLogger('operate').log(20, 'KEYSTONE TENANT_CREATE %s %s True successed.' % 
        (tenant_name, tenant_desc))
        return base.getid(nt)
    finally:
        pass

def tenant_delete(uuid):
    try:
        keystone = get_client1()
        keystone.tenants.delete(uuid)
    except:
        logging.getLogger('operate').log(30, 'KEYSTONE TENANT_DELETE failed %s.' % (uuid))
    else:
        logging.getLogger('operate').log(20, 'KEYSTONE TENANT_DELETE successful %s.' % (uuid))
    finally:
        pass

def add_tenant_user_role(tenant_id, user_id, role_id):
    res = None
    try:
        keystone = get_client1()
        res = keystone.roles.add_user_role(user_id, role_id, tenant_id)
    except:
        logging.getLogger('operate').log(30, 'KEYSTONE ADD_TENANT_USER_ROLE failed %s %s %s %s .' % (tenant_id, user_id, role_id, res))
    else:
        logging.getLogger('operate').log(20, 'KEYSTONE ADD_TENANT_USER_ROLE successful %s %s %s %s .' % (tenant_id, user_id, role_id, res))
    finally:
        return res

def remove_tenant_user_role(tenant_id, user_id, role_id):
    res = None
    try:
        keystone = get_client1()
        res = keystone.roles.remove_user_role(user_id, role_id, tenant_id)
    except:
        logging.getLogger('operate').log(30, 'KEYSTONE REMOVE_TENANT_USER failed %s %s %s %s.' % (tenant_id, user_id, role_id, res))
    else:
        logging.getLogger('operate').log(20, 'KEYSTONE REMOVE_TENANT_USER successful %s %s %s %s.' % (tenant_id, user_id, role_id, res))
    finally:
        return res
#
#
#
#
#
