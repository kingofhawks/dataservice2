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

# identity_service = "192.168.0.50:35
# identity_service = "192.168.0.50:35357"
# volume_service = "192.168.0.51:8776"
compute_service = "192.168.0.51:8774"
image_service = "192.168.0.50:9292"

def http_send(method, host, url, header, body):
    conn = httplib.HTTPConnection(host)
    conn.request(method, url, body, header)
    response = conn.getresponse()
    data = response.read()
    dict_res = json.loads(data)
    conn.close()
    return dict_res

def tenant_usage(token, tenant, start , end):
    method = 'GET'
    host = compute_service
    url = '/v2/%s/os-simple-tenant-usage?start=%s&end=%s' % (tenant, start, end)
    header = {"Content-Type": "application/json", "X-Auth-Token":token}
    useage = ''
    param = {}
    res = http_send(method, host, url, header, json.dumps(param))
    try:
        res['tenant_usages']
    except:
        res = None
    else:
        useage = res['tenant_usages']
    finally:
        pass
    
    
if __name__ == "__main__":
    start = datetime.datetime(2013, 6, 7, 10, 0, 0, 1).isoformat()
    end = datetime.datetime.now().isoformat()
    tenant_usage('ef94cce013a9494da252a93ad3991cf1', '86e5ae17b73749b3957886c5ad512ba0', start, end)
