# coding=utf-8
from novaclient.v1_1 import client
from novaclient.v1_1 import base
from novaclient import openstack
import datetime
import time



def getClient1():
    USER = 'test'
    PASS = '123456'
    TENANT_NAME = 'openstackDemo'
    AUTH_URL = 'http://192.168.110.120:35357/v2.0'
    OS_REGION_NAME = 'RegionOne'
    nc = client.Client(USER, PASS, TENANT_NAME, AUTH_URL)
    return nc

def getClient2():
    USER = 'admin'
    PASS = 'openstack'
    TENANT_NAME = 'adminTenant'
    AUTH_URL = 'http://192.168.0.106:5000/v2.0'
    nc = client.Client(USER, PASS, TENANT_NAME, AUTH_URL)
    return nc

def testNovaByClientOn96():
    USER = 'admin'
    PASS = '123456'
    TENANT_NAME = 'admin'
    AUTH_URL = 'http://192.168.0.96:5000/v2.0'
    nova = client.Client(USER, PASS, TENANT_NAME, AUTH_URL)
    print nova.servers.list()
    '''
    for s in nova.servers.list():
        oneServer = s
    myServer = nova.servers.get('a7ac05c6-801d-4262-bbda-9e9cb33202fd')
    print myServer
    print myServer.diagnostics()
    '''
    print nova.servers.list(False, {})

def testNovaByOpenStack():
    USER = 'admin'
    PASS = '123456'
    AUTH_URL = 'http://192.168.0.96:5000/v2.0'
    nova = openstack(USER, PASS, AUTH_URL)

def testnovaByClient():
    nova = getClient3()
    for f in nova.flavors.list():
        print f
    for fip in nova.floating_ip_pools.list():
        print fip
    for s in nova.servers.list():
        print s

    try:
        '''
        nova = getClient2()
        # print nova.flavors.list()
        for f in nova.flavors.list():
            print f
        # print nova.floating_ip_pools.list()
        for fip in nova.floating_ip_pools.list():
            print fip
        # print nova.images.list()
        for i in nova.images.list():
            print i
        # print nova.servers.list()
        for s in nova.servers.list():
            print s
        print nova.servers.list(detailed=True)
        # print nova.servers.get('147db751-1d12-49c0-ab85-211b2165514b')
        t2 = datetime.datetime.now()
        t1 = datetime.datetime(2013, 3, 1, 12, 12, 12, 12300)
        print nova.usage.list(t1, t2)
        '''
    except:
        print 'error'
    finally:
        print ' '


def testnova2():
    USER = 'admin'
    PASS = 'openstack'
    TENANT_NAME = 'adminTenant'
    AUTH_URL = 'http://192.168.0.106:5000/v2.0'
    nova = openstack(USER, PASS, AUTH_URL)
    nova.servers.list()

def testBase():
    '''
    list = ['a', 'b', 'c', 'd', 'e']
    for x in list:
        print x
    else:
        print 'finished!'
    '''
    # file iterator,best practice to read a file
    # and also the best loop form
    # 文件迭代器，读取文件的最佳实践
    '''
    for line in open('test.txt'):
        print line.upper()
    '''
    # dictionary
    # 字典迭代器
    '''
    testDict = {'name':'Chen Zhe', 'gender':'male'}
    for key in testDict:
        print key + ':' + testDict[key]
    '''
    # iterator in list comprehension
    # list comprehension中的迭代器
    testList = [line for line in open('test.txt')]
    print [line.upper() for line in open('test.txt')]
    # print testList

if __name__ == "__main__":
    tenant_usage('ef94cce013a9494da252a93ad3991cf1', '86e5ae17b73749b3957886c5ad512ba0')
    # testNovaByClientOn96()
    # testBase()
    # testnova2()
