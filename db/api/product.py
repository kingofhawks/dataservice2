#coding=utf-8
'''
Created on 2013-5-27

@author: YUWANG
'''
from django.db import connection
from db.models import *
import string


def list_serviceCategory():
    return serviceCategory.objects.all()


def list_productCategory():
    cursor = connection.cursor()
    cursor.execute("""select pc.id,pc.name,sc.name,pc.comment from productCategory pc,serviceCategory sc where pc.serviceCategoryId=sc.id""")
    productCategorys = cursor.fetchall()
    return productCategorys


def list_product():
    cursor = connection.cursor()
    cursor.execute("""select p.id,p.name,pc.name,p.isActive,p.price,p.unit from product p,productCategory pc where p.productCategoryId=pc.id""")
    products = cursor.fetchall()
    return products


def list_valueAdded_service():
    cursor = connection.cursor()
    cursor.execute("""select pc.id,pc.name,p.id,p.name from product p,productCategory pc where pc.serviceCategoryId='sec1001' and p.isActive='1' and pc.id=p.productCategoryId """)
    products = cursor.fetchall()
    return products


def add_serviceCategory(id, formValue):
    serviceCategoryInfo = serviceCategory(name=formValue.POST['name'], comment=formValue.POST['comment'])
    serviceCategoryInfo.save()
    return 1


def add_productCategory(id, formValue):
    productCategoryInfo = productCategory(name=formValue.POST['name'],
                                          serviceCategoryId=formValue.POST['serviceCategoryId'],
                                          comment=formValue.POST['comment'])
    productCategoryInfo.save()
    return 1


def add_product(id, formValue):
    productInfo = product(name=formValue.POST['name'],productCategoryId=formValue.POST['productCategory'],isActive=formValue.POST['isActive'],path=formValue.POST['path'],price=formValue.POST['price'],unit=formValue.POST['unit'],comment=formValue.POST['comment'])
    productInfo.save()
    return 1


def get_servCategId():
    if (serviceCategory.objects.count() == 0):
        id = "seC1000"
    else:
        maxId = serviceCategory.objects.order_by('-id')[0].id
        id = "seC"+str(string.atoi(maxId[3:])+1)
    return id


def get_prodCategId():
    if (productCategory.objects.count() == 0):
        id = "prC1000"
    else:
        maxId = productCategory.objects.order_by('-id')[0].id
        id = "prC"+str(string.atoi(maxId[3:])+1)
    return id


def get_productId():
    if (product.objects.count() == 0):
        id = "pro1000"
    else:
        maxId = product.objects.order_by('-id')[0].id
        id = "pro"+str(string.atoi(maxId[3:])+1)
    return id


def get_prodCategInfo(paraInfo):
    return productCategory.objects.filter(**paraInfo)


def get_servCategInfo(id):
    return serviceCategory.objects.filter(id=id)


def get_productDetail(id):
    cursor = connection.cursor()
    cursor.execute("""select p.id,p.name,pc.name,p.isActive,p.path,p.price,p.unit,p.comment from product p,productCategory pc where p.id=%s and p.productCategoryId=pc.id""",[id])
    productInfo = cursor.fetchall()
    return productInfo


def get_productInfo(paraInfo):
    return product.objects.filter(**paraInfo)


def count(obj):
    return obj.count()


def delete_serviceCategory(id):
    serviceCategory.objects.filter(id=id).delete()
    return 1


def delete_productCategory(id):
    productCategory.objects.filter(id=id).delete()
    return 1


def edit_serviceCategory(formValue):
    serviceCategory.objects.filter(id=formValue.POST['id']).update(name=formValue.POST['name'],comment=formValue.POST['comment'])
    return 1


def edit_productCategory(formValue):
    productCategory.objects.filter(id=formValue.POST['id']).update(name=formValue.POST['name'],serviceCategoryId=formValue.POST['serviceCategory'],comment=formValue.POST['comment'])
    return 1


def edit_product(formValue):
    product.objects.filter(id=formValue.POST['id']).update(name=formValue.POST['name'],productCategoryId=formValue.POST['productCategory'],isActive=formValue.POST['isActive'],path=formValue.POST['path'],price=formValue.POST['price'],unit=formValue.POST['unit'],comment=formValue.POST['comment'])
    return 1


def inactive_product(id):
    return product.objects.filter(id=id).update(isActive="0")
