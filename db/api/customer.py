'''
Created on 2013-5-24

@author: YUWANG
'''
from django.db import connection
from db.models import *
import string
import time


def list_customer():
    return customer.objects.all()


def list_customerGroup():
    return customerGroup.objects.all()


def get_customerInfo(id):
    return customer.objects.filter(id=id)


def get_customerGroupInfo(id):
    return customerGroup.objects.filter(id=id)


def edit_customerGroup(formValue):
    return customerGroup.objects.filter(id=formValue.POST['id']).update(name=formValue.POST['name'],discountId=formValue.POST['discount'],productId=formValue.POST.getlist('product'),comment=formValue.POST['comment'])


def edit_customer(formValue):
    customer.objects.filter(id=formValue.POST['id']).update(name=formValue.POST['name'],contactName=formValue.POST['contactName'],identification=formValue.POST['identification'],tel=formValue.POST['tel'],email=formValue.POST['email'],address=formValue.POST['address'],post=formValue.POST['post'],is_enterprise=formValue.POST['isEnterprise'],customerGroupId=formValue.POST['customerGroup'])
    return 1


def del_customer(id):
    customer.objects.filter(id=id).update(cancelDate=time.strftime('%Y-%m-%d',time.localtime(time.time())))


def get_accountInfo(paraInfo):
    return account.objects.filter(**paraInfo)


def get_cusGroupId():
    if (customerGroup.objects.count() == 0):
        id = "cuG1000"
    else:
        maxId = customerGroup.objects.order_by('-id')[0].id
        id = "cuG"+str(string.atoi(maxId[3:])+1)
    return id


def add_customerGroup(id, formValue):
    cusGroupInfo = customerGroup(name=formValue.POST['name'], discountId=formValue.POST['discountId'],productId=formValue.POST.getlist('product'),comment=formValue.POST['comment'])
    cusGroupInfo.save()
'''
def add_groupDiscServ(id,formValue):
    groupDiscServInfo = groupDiscountService(customerGroupId=id,discountId=formValue.POST['discountId'],productId=formValue.POST.getlist('product'))
    groupDiscServInfo.save()
'''