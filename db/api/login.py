'''
Created on 2013-5-15

@author: YUWANG
'''
#coding=utf-8

from django.http import *
from hashlib import md5
from db.models import sysAdmin


def login_auth(username, password):
    admin = sysAdmin.objects.filter(name=username)
    if admin:
        # get md5
        #pwd_md5=md5()
        #pwd_md5.update(password)
        cypher = sysAdmin().md5_password(password)
        print 'password****%s', (cypher)
        if admin[0].password == cypher:
            # match
            return "2"
            #html="<html><body>1</br>admin.name:%s,admin.password:%s</br>user:%s,pwd:%s</body></html>" %(admin.name,admin.password,username,pwd_md5.hexdigest())
            #return HttpResponse(html)
        else:
            return "3"
            #html="<html><body>0</br>admin.name:%s,admin.password:%s</br>user:%s,pwd:%s</body></html>" %(admin.name,admin.password,username,pwd_md5.hexdigest())
            #return HttpResponse(html)
    else:
        #the user does not exist
        return "1"
