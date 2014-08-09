#!/usr/bin/python

import httplib
import json

def http_send(method, url, body, params, headers):
    conn = httplib.HTTPConnection(url)
    conn.request(method, body, params, headers)
    response = conn.getresponse()
    data = response.read()
    dict_res = json.loads(data)
    conn.close()
    return dict_res

def send(method, url, body, params, headers):
    return http_send(method, url, body, params, headers)

if __name__ == "__main__":
    method = 'POST'
    url = "192.168.0.96:5000"
    body = '/v2.0/tokens'
    params = '''{"auth":{"passwordCredentials":{"username": "chuzhen", "password":"chuzhen"}, 
            "tenantName":"project1"}}'''
    headers = {"Content-Type": "application/json"}
    res = send(method, url, body, params, headers)
    print type(res)
    print res


'''
conn = httplib.HTTPConnection(url)
conn.request("POST", "/v2.0/tokens", params, headers)
response = conn.getresponse()
data = response.read()
dd = json.loads(data)
conn.close()
apitoken = dd['access']['token']['id']
print "Your token is: %s" % apitoken
'''
