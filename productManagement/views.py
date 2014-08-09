# Create your views here.
#coding=utf-8

from django.http import *
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_exempt
from db.models import *
from db.api.product import *
from utils.common import *

'''
    服务类型管理
'''


@csrf_exempt
def serviceCategorysIndex(request):
    serviceCategorys = list_serviceCategory()
    return render_to_response('productManagement/serviceCategoryIndex.html',locals())


@csrf_exempt
def addServiceCategory(request):
    #serviceCategoryId = get_servCategId()
    add_serviceCategory(None, request)

    return HttpResponseRedirect(reverse('productManagement.views.serviceCategorysIndex'))


def editServiceCategoryForm(request, pk):
    #serviceCategoryId = get_currentId(request)
    serviceCategoryInfo = get_servCategInfo(pk)

    return render_to_response('productManagement/editServiceCategoryForm.html',locals())


@csrf_exempt
def editServiceCategory(request):
    edit_serviceCategory(request)
    return HttpResponseRedirect(reverse('productManagement.views.serviceCategorysIndex'))


@csrf_exempt
def deleteServiceCategory(request, pk):
    #servCategId = get_currentId(request)
    productCateg_param = dict({"serviceCategoryId": pk})
    serviceCategoryInfo = get_prodCategInfo(productCateg_param)
    servCategNum = count(serviceCategoryInfo)

    if servCategNum == 0:
        delete_serviceCategory(pk)
        return HttpResponseRedirect(reverse('productManagement.views.serviceCategorysIndex'))
    else:
        outHtml = "<html><body>该服务类型 已有产品种类，不能删除</body></html>"
        return HttpResponse(outHtml)

'''
   产品种类管理
'''
@csrf_exempt
def productCategoryIndex(request):
    serviceCategorys = list_serviceCategory()
    productCategorys = list_productCategory()

    return render_to_response('productManagement/productCategoryIndex.html',locals())


@csrf_exempt
def addProductCategory(request):
    #productCategoryId = get_prodCategId()
    add_productCategory(None, request)
    return HttpResponseRedirect(reverse('productManagement.views.productCategoryIndex'))


def editProductCategoryForm(request, pk):
    #productCategoryId = get_currentId(request)
    prodCateg_param = dict({"id": pk})
    productCategoryInfo = get_prodCategInfo(prodCateg_param)
    serviceCategorys = list_serviceCategory

    return render_to_response('productManagement/editProductCategoryForm.html',locals())


@csrf_exempt
def editProductCategory(request):
    edit_productCategory(request)

    return HttpResponseRedirect(reverse('productManagement.views.productCategoryIndex'))


@csrf_exempt
def deleteProductCategory(request, pk):
    #prodCategId = get_currentId(request)
    product_param = dict({"productCategoryId": pk})

    if count(get_productInfo(product_param)) == 0:
        delete_productCategory(pk)
        return HttpResponseRedirect(reverse('productManagement.views.productCategoryIndex'))
    else:
        outHtml = "<html><body>该产品种类类型 已有产品，不能删除</body></html>" 
        return HttpResponse(outHtml)

'''
    产品管理
'''
@csrf_exempt
def productIndex(request):
    products = list_product()

    return render_to_response('productManagement/productIndex.html',locals())


def addProductForm(request):
    productCategorys = list_productCategory
    return render_to_response('productManagement/addProductForm.html',locals())


@csrf_exempt
def addProduct(request):
    #productId = get_productId()
    add_product(None, request)

    return HttpResponseRedirect(reverse('productManagement.views.productIndex'))


def productDetail(request, pk):
    #productId = get_currentId(request)
    productDetail = get_productDetail(pk)

    return render_to_response('productManagement/productDetail.html',locals())


def editProductForm(request, pk):
    #productId = get_currentId(request)
    productCategorys = list_productCategory
    product_param = dict({"id": pk})
    products = get_productInfo(product_param)

    return render_to_response('productManagement/editProductForm.html',locals())


@csrf_exempt
def editProduct(request):
    edit_product(request)

    return HttpResponseRedirect(reverse('productManagement.views.productIndex'))


@csrf_exempt
def inactiveProduct(request, pk):
    #productId = get_currentId(request)
    inactive_product(pk)

    return HttpResponseRedirect(reverse('productManagement.views.productIndex'))