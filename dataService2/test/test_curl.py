# coding:utf-8
import pycurl
 
c = pycurl.Curl()
c.setopt(c.URL, 'http://192.168.0.96:35357/v2.0/tenants')
# c.setopt(c.CONNECTTIMEOUT, 5)
# c.setopt(c.TIMEOUT, 8)
# c.setopt(c.COOKIEFILE, '')
c.setopt(c.FAILONERROR, True)
c.setopt(c.HTTPHEADER, ['X-Auth-Token:admin'])
# c.setopt(c.setopt

try:
    abc = c.perform()
except pycurl.error, error:
    errno, errstr = error
    print 'An error occurred: ', errstr
