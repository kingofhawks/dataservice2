import pycurl
import StringIO
import urllib

url = 'http://192.168.0.96:35357/v2.0/tokens'
# url = 'http://192.168.0.96:35357/v2.0/tenants'
head = ['Content-Type: application/json']
# head = ['X-Auth-Token:admin']
post_data_dic = {'auth':{'passwordCredentials':{'username': 'admin', 'password':'123456'}, 
                         'tenantId':'02023e0271504682b05598585ad3ac1c'}}
crl = pycurl.Curl()
crl.setopt(pycurl.VERBOSE, 1)
crl.setopt(pycurl.FOLLOWLOCATION, 1)
crl.setopt(pycurl.MAXREDIRS, 5)
crl.setopt(crl.HTTPHEADER, head)
# crl.setopt(pycurl.AUTOREFERER,1)
# crl.setopt(pycurl.CONNECTTIMEOUT, 60)
# crl.setopt(pycurl.TIMEOUT, 300)
# crl.setopt(pycurl.PROXY,proxy)
crl.setopt(pycurl.HTTPPROXYTUNNEL, 1)
# crl.setopt(pycurl.NOSIGNAL, 1)
crl.fp = StringIO.StringIO()
# crl.setopt(pycurl.USERAGENT, "dhgu hoho")
# Option -d/--data <data>   HTTP POST data
crl.setopt(crl.POSTFIELDS, urllib.urlencode(post_data_dic))
crl.setopt(pycurl.URL, url)
crl.setopt(crl.WRITEFUNCTION, crl.fp.write)
crl.perform()
tp = crl.fp.getvalue()
print tp
