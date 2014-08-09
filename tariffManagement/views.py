# Create your views here.
#coding=utf-8

from django.http import *
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_exempt
from db.api.tariff import *
from db.api.product import *
from utils.common import *
#from tables import discount,package
#from productManagement.tables import product
#from django.db import connection
#import string
#import json

'''
        折扣管理
'''


@csrf_exempt
def discountsIndex(request):
    discounts = list_discounts
    return render_to_response('tariffManagement/discountIndex.html', locals())


@csrf_exempt
def addDiscount(request):
    #discountId = get_discountId()
    discountInfo = add_discountInfo(None, request)

    return HttpResponseRedirect(reverse('tariffManagement.views.discountsIndex'))


def editDiscountForm(request, pk):
    #discountId = get_currentId(request)
    discount_param = dict({"id": pk})
    discountInfo = get_discountInfo(discount_param)

    return render_to_response('tariffManagement/editDiscountForm.html',locals())


@csrf_exempt
def editDiscount(request):
    edit_discount(request)

    return HttpResponseRedirect(reverse('tariffManagement.views.discountsIndex'))


@csrf_exempt
def inactiveDiscount(request, pk):
    #discountId = get_currentId(request)
    inactive_discount(pk)

    return HttpResponseRedirect(reverse('tariffManagement.views.discountsIndex'))

'''
    套餐管理
'''


@csrf_exempt
def packagesIndex(request):
    packages = list_package()

    return render_to_response('tariffManagement/packageIndex.html',locals())


def addPackageForm(request):
    products = list_product()
    return render_to_response('tariffManagement/addPackageForm.html',locals())


@csrf_exempt
def addPackage(request):
    #packageId = get_packageId()
    add_packageInfo(None, request)
    return HttpResponseRedirect(reverse('tariffManagement.views.packagesIndex'))


def editPackageForm(request, pk):
    #currentUrl = request.get_full_path()
    #packageId = 'pac'+currentUrl.split('/')[-1]
    #packageId = get_currentId(request)
    products = list_product()
    #products = product.objects.all()
    package_param = dict({"id": pk})
    packageInfo = get_packageInfo(package_param)
    #packageInfo=package.objects.filter(id=packageId)
    return render_to_response('tariffManagement/editPackageForm.html',locals())


@csrf_exempt
def editPackage(request):
    edit_packageInfo(request)
    return HttpResponseRedirect(reverse('tariffManagement.views.packagesIndex'))


@csrf_exempt
def inactivePackage(request, pk):
    #currentUrl = request.get_full_path()
    #packageId = 'pac'+currentUrl.split('/')[-1]
    #packageId = get_currentId(request)
    inactive_package(pk)

    return HttpResponseRedirect(reverse('tariffManagement.views.packagesIndex'))
