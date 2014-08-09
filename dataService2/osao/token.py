# coding=utf-8
import json
import urllib
import urllib2
import httplib

true = True
null = None

keystone_endpoint = '192.168.0.50:5000'
nova_endpoint = '192.168.0.51:8774'

def get_admin_token():
    admin_token = 'admin'
    return admin_token

def http_send(method, url, body, headers, params):
    conn = httplib.HTTPConnection(url)
    conn.request(method, body, params, headers)
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

# def get_user_token(userName, password, tenantUUID):
    # res = http_send('POST', '192.168.0.96:5000', '/v2.0/tokens', {"Content-Type": "application/json"},
        # '''{"auth":{"passwordCredentials":{"username": "%s", "password":"%s"},
        # "tenantName":"%s"}}''') % (userName, password, tenantUUID)
    # print res
    # return res

def get_tenant_token(userName, password, tenantUUID):
    method = 'POST'
    url = "192.168.0.50:5000"
    body = '/v2.0/tokens'
    headers = {"Content-Type": "application/json"}
    params = '''{"auth":{"passwordCredentials":{"username": "%s", "password":"%s"}, 
            "tenantId":"%s"}}''' % (userName, password, tenantUUID)
    res = http_send(method, url, body, headers, params)
    # res = http_send('POST', '192.168.0.50:5000', '/v2.0/tokens', {"Content-Type": "application/json"},
        # '{"auth":{"passwordCredentials":{"username": "%s", "password":"%s"},"tenantId":"%s"}}') % (
        # userName, password, tenantUUID)
    try:
        res['access']
    except:
        token = None
        print res['error']['message']
        print res['error']['code']
        print res['error']['title']
    else:
        token = res['access']['token']['id']
        # print res['access']['token']['id']
        # print res['access']['token']['expires']
    finally:
        pass
    return token, res

def test_send():
    method = 'POST'
    url = "192.168.0.96:5000"
    body = '/v2.0/tokens'
    params = '''{"auth":{"passwordCredentials":{"username": "chuzhen", "password":"chuzhen"}, 
            "tenantId":"1270311128c644ecbd89c15d25e192f2"}}'''
    headers = {"Content-Type": "application/json"}
    return http_send(method, url, body, headers, params)

if __name__ == "__main__":
    res = test_send()
    print type(res)
    print res
    try:
        res['access']
    except:
        # print res['error']
        print res['error']['message']
        print res['error']['code']
        print res['error']['title']
    else:
        print ['access']['token']['id']
        print ['access']['token']['expires']
        print ['access']['tenant']['id']
        print ['access']['tenant']['name']
        print ['access']['tenant']['desc']
    finally:
        ppp = {'access':
               {'token':
                {'expires': '2013-05-18T07:16:48Z',
                 'id': 'ff0fcd5b63204597989c7b9a8decc370',
                 'tenant':
                 {'enabled': True,
                  'description': 'project for test.',
                  'name': 'project1',
                  'id': '1270311128c644ecbd89c15d25e192f2'
                  }
                 },
                'user': 
                    {'username': 'chuzhen',
                     'roles_links': [],
                     'id': '75b6b04340f747b5b4ac4ec71c4f9c99',
                     'roles':[{'id': '44aaf30dbc6a4c929acff321f7e054c6', 'name': 'admin'}],
                     'name': 'chuzhen'
                     }
                }
               }
