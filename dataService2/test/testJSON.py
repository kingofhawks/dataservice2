# coding=utf-8
import commands

import urllib
import urllib2
import simplejson

def test2():
    # status, output = commands.getstatusoutput('''curl -d '{"auth":{"tenantName":"admin","passwordCredentials":{"username":"admin","password":"123456"}}}' -H "Content-type:application/json" http://192.168.0.96:35357/v2.0/tokens ''')
    output = commands.getoutput('''curl -I -d '{"auth":{"tenantName":"admin","passwordCredentials":{"username":"admin","password":"123456"}}}' -H "Content-type:application/json" http://192.168.0.96:35357/v2.0/tokens ''')
    output=commands.getoutput('ls -l')
    print output
    print type(output)
    
def test1():
    url = 'http://192.168.0.96:35357/v2.0/tokens'
    values = {"auth":{"tenantName":"admin", "passwordCredentials":{"username":"admin", "password":"123456"}}}
    headers = { 'Content-type' : 'application/json' }
    data = urllib.urlencode(values)
    req = urllib2.Request(url, data, headers)
    response = urllib2.urlopen(req)
    the_page = response.read()
    print the_page
    '''
    req = urllib2.Request("http://192.168.0.96:35357/v2.0/tokens",
                          '{"auth":{"tenantName":"admin","passwordCredentials":{"username":"admin","password":"123456"}}}',
                          "Content-type:application/json")
    opener = urllib2.build_opener()
    f = opener.open(req)
    simplejson.load(f)
    '''

if __name__ == "__main__":
    test2()

'''
def test3():
    headers = {
    'Host': 'digitalvita.pitt.edu',
    'Connection': 'keep-alive',
    'Content-Length': '325', 
    'Origin': 'https://digitalvita.pitt.edu',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_4) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1',
    'Content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Accept': 'text/javascript, text/html, application/xml, text/xml, */*',
    'Referer': 'https://digitalvita.pitt.edu/index.php',
    'Accept-Encoding': 'gzip,deflate,sdch',
    'Accept-Language': 'en-US,en;q=0.8',
    'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
    'Cookie': 'PHPSESSID=lvetilatpgs9okgrntk1nvn595'
}

data = {
    'action': 'search',
    'xdata': '<search id="1"><context type="all" /><results><ordering>familyName</ordering><pagesize>100000</pagesize><page>1</page></results><terms><name>d</name><school>All</school></terms></search>',
    'request': 'search'
}

data = urllib.urlencode(data) 
print data 
req = urllib2.Request('https://digitalvita.pitt.edu/dispatcher.php', data, headers) 
response = urllib2.urlopen(req)
the_page = response.read()
'''

