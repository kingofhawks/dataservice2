'''
Created on 2013-5-22

@author: YUWANG
'''
from django.db import connection
from db.models import adminGroup, sysAdmin
import string


def get_id(table):
    if table == "adminGroup":
        if (adminGroup.objects.count() == 0):
            id = "admin1000"
        else:
            maxId = adminGroup.objects.exclude(id="superAdmin").order_by('-id')[0].id
            id = "admin"+str(string.atoi(maxId[5:])+1)
    elif table == "sysAdmin":
        if sysAdmin.objects.count() == 0:
            id = "sys1000"
        else:
            maxId = sysAdmin.objects.order_by('-id')[0].id
            print 'maxId****%s', (maxId)
            id = "sys"+str(string.atoi(maxId[3:])+1)

    return id


def insert_admin(id, formValue, table):
    if table == "adminGroup":
        adminInfo = adminGroup(name=formValue.POST['name'], comment=formValue.POST['comment'])
        adminInfo.save()
        return 1
    elif table == "sysAdmin":
        cypher = sysAdmin().md5_password(formValue.POST['pwd'])
        adminInfo = sysAdmin(name=formValue.POST['name'], password=cypher, email=formValue.POST['email'], adminGroupId=formValue.POST['group'])
        adminInfo.save()
        return 1


def list_admin(table):
    if table == "adminGroup":
        return adminGroup.objects.all()
    elif table == "sysAdmin":
        cursor = connection.cursor()
        cursor.execute(""" select s.id,s.name,s.email,a.name from sysAdmin s,adminGroup a where s.adminGroupId=a.id """)
        result = cursor.fetchall()
        return result


def get_currentId(url, table):
    currentUrl = url.get_full_path()

    if table == "adminGroup":
        id = 'admin'+currentUrl.split('/')[-1]
    elif table == "sysAdmin":
        id = 'sys'+currentUrl.split('/')[-1]

    return id 


def get_adminInfo(id, table):
    if table == "adminGroup":
        return adminGroup.objects.filter(id=id)
    elif table == "sysAdmin":
        return sysAdmin.objects.filter(id=id)


def edit_adminInfo(formValue, table):
    if table == "adminGroup":
        adminGroup.objects.filter(id=formValue.POST['id']).update(name=formValue.POST['name'], comment=formValue.POST['comment'])
        return 1

    elif table == "sysAdmin":
        cypher = sysAdmin().md5_password(formValue.POST['password'])
        sysAdmin.objects.filter(id=formValue.POST['id']).update(name=formValue.POST['name'], 
                                                                password=cypher,
                                                                email=formValue.POST['email'],
                                                                adminGroupId=formValue.POST['group'])
        return 1


def delete_admin(id, table):
    if table == "adminGroup":
        if not get_adminInfo(id, "sysAdmin"):
            return adminGroup.objects.filter(id=id).delete()
    elif table == "sysAdmin":
        return sysAdmin.objects.filter(id=id).delete()
