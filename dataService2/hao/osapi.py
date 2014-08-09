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

# identity_service = "192.168.0.50:35357"
# volume_service = "192.168.0.51:8776"
compute_service = "192.168.0.51:8774"
image_service = "192.168.0.50:9292"

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

def server_create(token, tenant, name, image, flavor, metadata):
    method = 'POST'
    host = compute_service
    url = '/v2/%s/servers' % (tenant)
    header = {"Content-Type": "application/json", "X-Auth-Token":token}
    param = {"server": 
              {
               "name": name,
               "imageRef": image,
               "flavorRef": flavor,
               "metadata": metadata,
               "security_group":"new_security",
               "personality": [],
               }
              }
    res = http_send(method, host, url, header, json.dumps(param))
    '''
    {u'server': 
        {
        u'links': [
            {
            u'href': u'http://192.168.0.51:8774/v2/86e5ae17b73749b3957886c5ad512ba0/servers/be20343e-99b7-40fe-ab98-f185885122cb', 
            u'rel': u'self'
            }, 
            {
            u'href': u'http://192.168.0.51:8774/86e5ae17b73749b3957886c5ad512ba0/servers/be20343e-99b7-40fe-ab98-f185885122cb', 
            u'rel': u'bookmark'
            }
            ], 
        u'OS-DCF:diskConfig': u'MANUAL', 
        u'id': u'be20343e-99b7-40fe-ab98-f185885122cb', 
        u'security_groups': [{u'name': u'default'}], 
        u'adminPass': u'7w4EoW8VVSwY'
        }
    }
    '''
    '''
    {u'badRequest': {u'message': u'Server name is an empty string', u'code': 400}}
    '''
    try:
        code = 200
        message = res['server']
    except:
        try:
            code = res['badRequest']['code']
            message = res['badRequest']
        except:
            code = 0
            message = 0
    else:
        pass
    finally:
        pass
    return code, message

def server_delete(token, tenant, server):
    method = 'DELETE'
    host = compute_service
    url = '/v2/%s/servers/%s' % (tenant, server)
    header = {"Content-Type": "application/json", "X-Auth-Token":token}
    res = http_send2(method, host, url, header, None)
    return res.status, res.reason

def floating_ip_associate(token, tenant, ip, server):
    method = 'POST'
    host = compute_service
    url = '/v2/%s/servers/%s/action' % (tenant, server)
    headers = {"Content-Type":"application/json", "X-Auth-Token":token}
    param = {
           "addFloatingIp": {
                             "address": ip
                            }
           }
    res = http_send2(method, host, url, headers, json.dumps(param))
    return res.status, res.reason

def server_list(token, tenant):
    method = 'GET'
    host = compute_service
    url = '/v2/%s/servers/detail' % (tenant)
    headers = {"Content-Type": "application/json", "X-Auth-Token":token}
    res = http_send(method, host, url, headers, None)
    ins_list = []
    try:
        for server in res['servers']:
            server.setdefault('task_state', server['OS-EXT-STS:task_state'])
            ins_list.append(server)
    except:
        ins_list = []
    else:
        pass
    finally:
        pass
    return ins_list
