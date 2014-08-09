'''
Created on 2013-1-21

@author: YUWANG
'''
#--coding=utf-8--

# Create your views here.
from django.http import *
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_exempt
from db.api.customer import *
from db.api.tariff import *
from db.api.product import *
from utils.common import *

# for test
#def hello(request):
#    return HttpResponse("Hello world")


@csrf_exempt
def customerIndex(request):
    customers = list_customer()
    return render_to_response('usersManagement/customerIndex.html', locals())

'''
    customer
'''
def customerDetail(request):
    customerId = get_currentId(request)
    customerInfo = get_customerInfo(customerId)
    customerGroupInfo = get_customerGroupInfo(customerInfo[0].customerGroupId)
    customerGroupName = customerGroupInfo[0].name
    return render_to_response('usersManagement/customerDetail.html',locals())


def addCustomerForm(request):
    customerGroups = list_customerGroup()

    return render_to_response('usersManagement/addCustomerform.html',locals())

'''
@csrf_exempt
def addCustomer(request):
    customerId=get_customerId()
    if request.method == 'POST':
        if (customer.objects.count()== 0):
            customerId = "cus1000"
        else:
            maxId = customer.objects.order_by('-id')[0].id
            customerId = "cus"+str(string.atoi(maxId[3:])+1)
        
    customerInfo=customer(id=customerId,name=request.POST['name'],contactName=request.POST['contactName'],identification=request.POST['identification'],tel=request.POST['tel'],email=request.POST['email'],address=request.POST['address'],post=request.POST['post'],createDate=time.strftime('%Y-%m-%d',time.localtime(time.time())),is_enterprise=request.POST['isEnterprise'],customerGroupId=request.POST['customerGroup'])
    customerInfo.save()
    return HttpResponseRedirect(reverse('usersManagement.views.customerIndex'))
'''


def EditCustomerForm(request):
    customerId = get_currentId(request)
    customerInfo = get_customerInfo(customerId)
    customerGroups = list_customerGroup()

    return render_to_response('usersManagement/editCustomerform.html',locals())


@csrf_exempt
def editCustomer(request):
    edit_customer(request)
    return HttpResponseRedirect(reverse('usersManagement.views.customerIndex'))


@csrf_exempt
def delCustomer(request):
    customerId = get_currentId(request)
    account_param = dict({"customerId": customerId, "cancelDate": None})
    if get_accountInfo(account_param):
        return HttpResponse("no")
    else:
        del_customer(customerId)
        #customer.objects.filter(id=customerId).update(cancelDate=time.strftime('%Y-%m-%d',time.localtime(time.time())))
        return HttpResponseRedirect(reverse('usersManagement.views.customerIndex'))

'''
   account
'''
   
   
@csrf_exempt
def accountIndex(request):
    id = get_currentId(request)
    account_param = dict({'customerId': id})
    accounts = get_accountInfo(account_param)
    #accounts = account.objects.filter(customerId=id)
    return render_to_response('usersManagement/accountIndex.html',locals())


'''
customerGroup
'''


@csrf_exempt
def customerGroupsIndex(request):
    customerGroups = list_customerGroup()
    return render_to_response('usersManagement/customerGroupsIndex.html', locals())


def addCustomerGroupForm(request):
    #id=get_currentId(request)
    discount_param = dict({'isActive': "1"})
    discounts = get_discountInfo(discount_param)
    prodCateg_param = dict({"serviceCategoryId": "sec1001"})
    productCategorys = get_prodCategInfo(prodCateg_param)
    products = list_valueAdded_service()

    return render_to_response('usersManagement/addCustomerGroupForm.html', locals())


@csrf_exempt
def addCustomerGroup(request):
    #cusGroupId = get_cusGroupId()
    add_customerGroup(None, request)

    return HttpResponseRedirect(reverse('usersManagement.views.customerGroupsIndex'))


def editCustomerGroupForm(request, pk):
    #customerGroupId = get_currentId(request)
    discount_param = dict({'isActive': "1"})
    discounts = get_discountInfo(discount_param)
    products = list_valueAdded_service()
    customerGroupInfo = get_customerGroupInfo(pk)

    return render_to_response('usersManagement/editCustomerGroupform.html',locals())


@csrf_exempt
def editCustomerGroup(request):
    edit_customerGroup(request)
    return HttpResponseRedirect(reverse('usersManagement.views.customerGroupsIndex'))

"""
@csrf_exempt
def addCustomerAccount(request):
    if (account.objects.count()== 0):
        accountId = "acc1000"
    else:
        maxId = account.objects.order_by('-id')[0].id
        accountId = "acc"+str(string.atoi(maxId[3:])+1)
    
    accountInfo = account(id=accountId,customerId=request.POST['customerId'],payKey=request.POST['payKey'],openDate=time.strftime('%Y-%m-%d',time.localtime(time.time())),openInfo=request.POST['openInfo'],comment=request.POST['comment'])
    accountInfo.save()
    
    return HttpResponseRedirect(reverse('usersManagement.views.customerIndex'))


@csrf_exempt
def cancelAccount(request):
    account.objects.filter(id=request.POST['accountId']).update(cancelDate=time.strftime('%Y-%m-%d',time.localtime(time.time())))
    return HttpResponseRedirect(reverse('usersManagement.views.customerIndex'))
"""
