# coding=utf-8
from keystoneclient.v2_0 import client
from keystoneclient import base
from keystoneclient.v2_0 import users
import datetime
import time

TOKEN = 'admin'
ENDPOINT = 'http://192.168.110.120:35357/v2.0'

USER = 'adminUser'
PASS = '123456'
TENANT_NAME = 'openstackDemo'
AUTH_URL = 'http://192.168.110.120:5000/v2.0'
    
# TOKEN = 'admin'
# ENDPOINT = 'http://192.168.110.120:35357/v2.0'
    
# USER = 'admin'
# PASS = 'openstack'
# TENANT_NAME = 'adminTenant'
# AUTH_URL = 'http://192.168.0.106:5000/v2.0'
def get_client1():
    TOKEN = 'admin'
    ENDPOINT = 'http://192.168.0.96:35357/v2.0'
    return client.Client(token=TOKEN, endpoint=ENDPOINT)

def get_client2():
    USER = 'admin'
    PASS = 'openstack'
    TENANT_NAME = 'adminTenant'
    AUTH_URL = 'http://192.168.0.106:5000/v2.0'
    return client.Client(username=USER, password=PASS, tenant_name=TENANT_NAME, auth_url=AUTH_URL)

def testKeystone():
    keystone = client.Client(username=USER, password=PASS, tenant_name=TENANT_NAME, auth_url=AUTH_URL)
    # print keystone.users.list()
    for u in keystone.users.list():
        print u 
    # print keystone.tenants.list()
    for t in keystone.tenants.list():
        print t
    # print keystone.instance
    # print keystone.roles.list()
    for r in keystone.roles.list():
        print r
    # print keystone.services.list()
    for s in keystone.services.list():
        print s
    # print keystone.endpoints.list()
    for e in keystone.endpoints.list():
        print e
    print keystone.users.get('3bb7beb96425462cb3f2995b7a964f81')

def k_createUser():
    keystone = client.Client(token=TOKEN, endpoint=ENDPOINT)
    newP = keystone.users.create('nameNNN6', 'passwordNNN', 'emailNNN', None, True)
    print newP
    print 'getid'
    newpid = base.getid(newP)
    print newpid
    print 'del'
    print keystone.users.delete(newpid)
    

def k_deleteUser():
    keystone = client.Client(token=TOKEN, endpoint=ENDPOINT)
    pp = keystone.users.delete('cf6e208dfea94ef8bbc615d2332153e8')
    
def k_getID():
    # pp = base.getid('adminUser')
    keystone = client.Client(username=USER, password=PASS, tenant_name=TENANT_NAME, auth_url=AUTH_URL)
    pp = keystone.users.get('c1fef9be9f1d4efc99ef5ef9fc22d01d')
    p2 = keystone.users.get('cf6e208dfea94ef8bbc615d2332153e8')
    print pp
    print p2

def test():
    # abc = 0
    try:
        abc = 123
        print abc
    except:
        print 'except'
        print abc
    else:
        print 'else'
        print abc

def user_create(name, password, email):
    keystone = get_client1()
    np = ''
    print type(np)
    try:
        np = keystone.users.create(name, password, email, None, True)
    except:
        print 'error'
        print type(np)
    else:
        print 'else'
        print type(np)
        print base.getid(np)

def tenant_create(tenant_name, tenant_desc):
    keystone = get_client1()
    nt = keystone.tenants.create(tenant_name, tenant_desc, True)
    print type(nt)
    print nt
    print base.getid(nt)

def tenant_delete(uuid):
    keystone = get_client1()
    keystone.tenants.delete(uuid)

def add_tenant_user_role(tenant_id, user_id, role_id):
    keystone = get_client1()
    print 'add_tenant_user_role'
    res = keystone.roles.add_user_role(user_id, role_id, tenant_id)
    return res

def remove_tenant_user(tenant_id, user_id, role_id):
    keystone = get_client1()
    keystone.tenants.remove_user(self, tenant, user, role)
    print keystone.roles.remove_user_role(user_id, role_id, tenant_id)
    print 'remove_tenant_user'

def user_detail(user):
    keystone = get_client1()
    u = keystone.users.list()
    for i in range(len(u)):
        print u[i]
            

if __name__ == "__main__":
    user_id = '75b6b04340f747b5b4ac4ec71c4f9c99'  # chuzhen
    tenant_id = '0d546adf12a24538aa367a87ec139c14'  # yongleadmin
    role_id = '91101c304619431f8eeb7cbea875bdfb'  # member
    user_detail('86e5ae17b73749b3957886c5ad512ba0')
    # remove_tenant_user('5af79b73f9b44ee19570e989b9eb04bd', '75b6b04340f747b5b4ac4ec71c4f9c99', '44aaf30dbc6a4c929acff321f7e054c6')
    # tenant_delete('5af79b73f9b44ee19570e989b9eb04bd')
    '''
    try:
        # rrr = add_tenant_user_role(tenant_id, user_id, role_id)
        rrr = remove_tenant_user(tenant_id, user_id, role_id)
    except:
        print 'except'
    else:
        print 'right'
    finally:
        print 'finally'
    '''
    # remove_tenant_user(tenant_id, user_id, role_id)
    # tenant_create('yongleadmin','shiyongadmintoken')
    # tenant_create('fasdgjaskgja','ceshi diyi ge')
    # tenant_delete('8c1a95c8903847139f9ea68b67764a60')
    # user_create('abc3', 'def', 'cpa@11.com')
