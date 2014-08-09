# coding:utf-8
import pycurl
import urllib
import StringIO
import json

def yi():
    true = True
    null = None
    c = pycurl.Curl()
    c.setopt(pycurl.URL, 'http://192.168.0.96:35357/v2.0/tenants')
    c.setopt(c.HTTPHEADER, ['X-Auth-Token:admin'])
    # c.setopt(pycurl.POST, 1)
    # c.setopt(pycurl.POSTFIELDS, "request=%s" % str('wrapper'))
    b = StringIO.StringIO()
    c.setopt(pycurl.WRITEFUNCTION, b.write)
    c.perform()
    n_data = eval(b.getvalue())
    b.close()
    c.close()
    print n_data

def er():
    true = True
    null = None
 #   data = {"auth":{"passwordCredentials":{"username": "admin", "password":"123456"}, "tenantId":"02023e0271504682b05598585ad3ac1c"}}
    data = {"auth":{"tenantName":"adminTenant", "passwordCredentials":{"username": "admin", "password":"123456"}}}
    # print data
    # data_encoded = urllib.urlencode(data)
    data_encoded = json.dumps(data)
    head = ['Content-Type: application/json']
    # url = 'http://192.168.0.96:35357/v2.0/tokens'
    url = 'http://192.168.0.101:8000/login/'
    
    b = StringIO.StringIO()
    c = pycurl.Curl()
    c.setopt(pycurl.URL, url)
    c.setopt(pycurl.POST, 1)
    c.setopt(c.HTTPHEADER, head)
    c.setopt(pycurl.POSTFIELDS, data_encoded)
    c.setopt(pycurl.WRITEFUNCTION, b.write)
    c.perform()
    # result = eval(b.getvalue())
    result = b.getvalue()
    b.close()
    c.close()
    print result

if __name__ == "__main__":
    # yi()
    er()
