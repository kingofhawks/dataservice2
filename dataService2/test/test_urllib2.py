# coding:utf-8
import urllib
import urllib2
import json

true = True
null = None
# url = 'http://192.168.0.96:35357/v2.0/tenants'
url = 'http://192.168.0.96:35357/v2.0/tokens'
# user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
# values = {'name' : 'Michael Foord',       'location' : 'Northampton',        'language' : 'Python' }
data = {"auth":{"passwordCredentials":{"username": "chuzhen", "password":"chuzhen"}, "tenantName":"project1"}}

# headers = {'X-Auth-Token':'admin'}
header = {'Content-Type': 'application/json'}

# print urllib.quote(urllib.urlencode(data))
request = urllib2.Request(url, json.dumps(data), header)
# request.add_header('Content-Type', 'application/json')
# request.add_data(json.dumps(data))

retval = urllib2.urlopen(request)

# print request.read()
# params=urllib.urlencode({'spam':1,'eggs'})

# data = urllib.urlencode(values)
# req = urllib2.Request(url, data, headers)
# response = urllib2.urlopen(req)
res = retval.read()
print res
n_data = eval(res)
print type(n_data)
print n_data
