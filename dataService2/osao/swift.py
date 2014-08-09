# coding=utf-8
import json
import urllib
import urllib2
import httplib
import logging
import datetime
import time

true = True
null = None

identity_service = "http://192.168.0.50:5000/v2.0"
# object_store = "http://192.168.0.55:8888/v1/AUTH_tenant_id"
object_store = "192.168.0.55:8888"
volume_service = "http://192.168.0.51:8776/v1/tenant_id"
image_service = "http://192.168.0.50:9292/v1"
compute_service = "http://192.168.0.51:8774/v2/tenant_id"

def http_send(method, host, url, header, body):
    conn = httplib.HTTPConnection(host)
    conn.request(method, url, body, header)
    response = conn.getresponse()
    data = response.read()
    try:
        dict_res = json.loads(data)
    except:
        dict_res = {}
    else:
        pass
    finally:
        conn.close()
    return dict_res

def http_send2(method, host, url, header, body):
    conn = httplib.HTTPConnection(host)
    conn.request(method, url, body, header)
    response = conn.getresponse()
    conn.close()
    return response

def get_containerList(token, tenant):
    method = 'GET'
    host = object_store
    url = '/v1/AUTH_%s?format=json' % (tenant)
    headers = {"X-Auth-Token":token}
    res = http_send(method, host, url, headers, None)
    try:
        container_list = res
    except:
        container_list = []
    return container_list

def get_fileList(token, tenant, container, file):
    method = 'GET'
    host = object_store
    url = '/v1/AUTH_%s/%s?format=json' % (tenant, container)
    # print url
    headers = {"X-Auth-Token":token}
    res = http_send(method, host, url, headers, None)
    # print res
    file_list = []
    folder_list = []
    try:
        # print file
        for i in range(len(res)):
            n_file = {
                    'name':res[i]['name'],
                    'type':res[i]['content_type'],
                    'byte':res[i]['bytes'],
                    'hash':res[i]['hash'],
                    'modified':res[i]['last_modified'],
                  }
            if(len(file) > 0):
                if(n_file['name'].find(file + '/') > -1):
                    # print n_file['name']
                    n_file['name'] = n_file['name'][len(file) + 1:]
                    # print n_file['name']
                    if(n_file['name'].find('/') == -1):
                        if(n_file['type'] == 'application/directory'):
                            folder_list.append(n_file)
                        else:
                            file_list.append(n_file)
            else:
                if(n_file['name'].find('/') == -1):
                    if(n_file['type'] == 'application/directory'):
                        folder_list.append(n_file)
                    else:
                        file_list.append(n_file)
    except:
        pass
    else:
        pass
    return folder_list, file_list

def get_fileList2(token, tenant, container, path):
    method = 'GET'
    host = object_store
    url = '/v1/AUTH_%s/%s?format=json' % (tenant, container)
    # print url
    headers = {"X-Auth-Token":token}
    res = http_send(method, host, url, headers, None)
    # print res
    file_list = []
    folder_list = []
    try:
        for i in range(len(res)):
            n_file = {
                    'name':res[i]['name'],
                    'type':res[i]['content_type'],
                    'byte':res[i]['bytes'],
                    'hash':res[i]['hash'],
                    'modified':res[i]['last_modified'],
                  }
            if(n_file['name'].find('/') == -1):
                if(n_file['type'] == 'application/directory'):
                    folder_list.append(n_file)
                else:
                    file_list.append(n_file)
        # print res
    except:
        pass
    else:
        pass
    return folder_list, file_list

def get_metadata(token, tenant):
    method = 'HEAD'
    host = object_store
    url = '/v1/AUTH_%s' % (tenant)
    headers = {"X-Auth-Token":token}
    res = http_send2(method, host, url, headers, None)
    try:
        res = res.getheaders()
        date = time = container_count = object_count = None
        for i in range(len(res)):
            if(res[i][0] == 'date'):
                date = res[i][1]
            if(res[i][0] == 'x-account-object-count'):
                object_count = res[i][1]
            if(res[i][0] == 'x-timestamp'):
                time = res[i][1]
            if(res[i][0] == 'x-account-container-count'):
                container_count = res[i][1]
            if(res[i][0] == 'x-account-bytes-used'):
                bytes_used = res[i][1]
        meta = {
                'date':date,
                'time':time,
                'object_count':object_count,
                'container_count':container_count,
                'bytes':bytes_used,
                }
    except:
        meta = {}
    return meta

def get_ContainerMetadata(token, tenant, container):
    method = 'HEAD'
    host = object_store
    url = '/v1/AUTH_%s/%s' % (tenant, container)
    headers = {"X-Auth-Token":token}
    res = http_send2(method, host, url, headers, None)
    try:
        res = res.getheaders()
        date = time = container_count = object_count = None
        for i in range(len(res)):
            if(res[i][0] == 'date'):
                date = res[i][1]
            if(res[i][0] == 'x-container-object-count'):
                object_count = res[i][1]
            if(res[i][0] == 'x-timestamp'):
                time = res[i][1]
            if(res[i][0] == 'x-container-bytes-used'):
                bytes_used = res[i][1]
        meta = {
                'date':date,
                'time':time,
                'object_count':object_count,
                'bytes':bytes_used,
                }
    except:
        meta = {}
    return meta

def container_create(token, tenant, container_name):
    method = 'PUT'
    host = object_store
    url = '/v1/AUTH_%s/%s' % (tenant, container_name)
    headers = {"X-Auth-Token":token}
    response = http_send2(method, host, url, headers, None)
    return response.status, response.reason

def container_delete(token, tenant, container_name):
    method = 'DELETE'
    host = object_store
    url = '/v1/AUTH_%s/%s' % (tenant, container_name)
    headers = {"X-Auth-Token":token}
    response = http_send2(method, host, url, headers, None)
    return response.status, response.reason

def folder_create(token, tenant, container_name, folder_name):
    method = 'PUT'
    host = object_store
    url = '/v1/AUTH_%s/%s/%s' % (tenant, container_name, folder_name)
    headers = {"X-Auth-Token":token,
               'content-type': 'application/directory',
               'content-length': 0}
    response = http_send2(method, host, url, headers, None)
    return response.status, response.reason

def folder_delete(token, tenant, container_name, folder_name):
    method = 'DELETE'
    host = object_store
    url = '/v1/AUTH_%s/%s/%s' % (tenant, container_name, folder_name)
    headers = {"X-Auth-Token":token}
    response = http_send2(method, host, url, headers, None)
    return response.status, response.reason

def file_delete(token, tenant, container_name, file_name):
    method = 'DELETE'
    host = object_store
    url = '/v1/AUTH_%s/%s/%s' % (tenant, container_name, file_name)
    print url
    headers = {"X-Auth-Token":token}
    response = http_send2(method, host, url, headers, None)
    return response.status, response.reason

def get_list(token, tenant, container):
    method = 'GET'
    host = object_store
    if(container == '/'):
        url = '/v1/AUTH_%s?format=json' % (tenant)
    else:
        url = '/v1/AUTH_%s/%s?format=json' % (tenant, container)
    headers = {"X-Auth-Token":token}
    res = http_send(method, host, url, headers, None)
    # print res

if __name__ == '__main__':
    token = '5d7747b6a034486193cd3ba0621b7a49'
    tenant = '86e5ae17b73749b3957886c5ad512ba0'
    container = 'test'
    file = 'folder/9'
    file_delete(token, tenant, container, file)
    



