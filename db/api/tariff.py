'''
Created on 2013-5-27

@author: YUWANG
'''
from django.db import connection
from db.models import *
import string


def list_discounts():
    return discount.objects.all()


def list_package():
    return package.objects.all()


def add_discountInfo(id, formValue):
    discountInfo = discount(discountValue=formValue.POST['discountValue'],isActive=formValue.POST['isActive'],comment=formValue.POST['comment'])
    discountInfo.save()
    return 1


def add_packageInfo(id, formValue):
    packageInfo = package(name=formValue.POST['name'],packageDetail=formValue.POST.getlist('productId'),timeLimit=formValue.POST['timeLimit'],price=formValue.POST['price'],isActive=formValue.POST['isActive'],comment=formValue.POST['comment'])
    packageInfo.save()
    return 1


def get_discountId():
    if (discount.objects.count() == 0):
        id = "dis1000"
    else:
        maxId = discount.objects.order_by('-id')[0].id
        id = "dis"+str(string.atoi(maxId[3:])+1)
    return id


def get_packageId():
    if (package.objects.count() == 0):
        id = "pac1000"
    else:
        maxId = package.objects.order_by('-id')[0].id
        id = "pac"+str(string.atoi(maxId[3:])+1)
    return id

'''
def get_currentID(url):
    currentUrl = url.get_full_path()
    id = currentUrl.split('/')[-1]
    return id
'''


def get_discountInfo(paraInfo):
    return discount.objects.filter(**paraInfo)


def get_packageInfo(paraInfo):
    return package.objects.filter(**paraInfo)


def edit_discount(formValue):
    discount.objects.filter(id=formValue.POST['id']).update(discountValue=formValue.POST['discountValue'],isActive=formValue.POST['isActive'],comment=formValue.POST['comment'])
    return 1


def edit_packageInfo(formValue):
    package.objects.filter(id=formValue.POST['id']).update(name=formValue.POST['name'],packageDetail=formValue.POST.getlist('productId'),timeLimit=formValue.POST['timeLimit'],price=formValue.POST['price'],isActive=formValue.POST['isActive'],comment=formValue.POST['comment'])
    return 1


def inactive_discount(id):
    discount.objects.filter(id=id).update(isActive="0")
    return 1


def inactive_package(id):
    package.objects.filter(id=id).update(isActive="0")
    return 1
