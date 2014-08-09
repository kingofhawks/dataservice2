#!/usr/bin/env python
import httplib
import json
from urlparse import urlparse, urlunparse, urljoin
from urllib import quote
# from eventlet.green.httplib import HTTPConnection
'''
def http_connection(url):
    parsed = urlparse(url)
    conn = HTTPConnection(parsed.netloc)
    return parsed, conn

def get_object():
    url, token = get_auth()
    parsed, conn = http_connection(url)
    path = '%s/%s/%s' % (parsed.path, quote('myfile'), quote('asd.txt'))
    method = 'GET'
    headers = {'X-Auth-Token': token}
    conn.request(method, path, '', headers)
    resp = conn.getresponse()
    body = resp.read()
    print body
'''

def get_auth():
    url = 'http://192.168.0.50:5000/v2.0/'
    body = {'auth': {'passwordCredentials': {'password': 'dscp1',
        'username':'123456'}, 'tenantName': 'dscp1_t1'}}
    token_url = urljoin(url, "tokens")
    resp, body = json_request("POST", token_url, body=body)
    token_id = None
    try:
        url = None
        catalogs = body['access']["serviceCatalog"]
        for service in catalogs:
            if service['type'] == 'object-store':
                url = service['endpoints'][0]['publicURL']
        token_id = body['access']['token']['id']
    except(KeyError, IndexError):
        print Error
    print url, token_id
    return url, token_id


if __name__ == '__main__':
    # get_object()
    get_auth()
