# Create your views here.

from django.http import *
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_exempt
from db.api.transactionBill import *
from utils.common import *
#from db.tables import *
#from tables import transactionBill
#from usersManagement.tables import customer,account
#from django.db import connection

@csrf_exempt
def billIndex(request):
    transactions=list_transactionBill()
    return render_to_response('transactionBillManagement/billIndex.html',locals())

@csrf_exempt
def search(request):
    # account
    conditions=get_searchConditions(request)
    '''
        account
    '''
    if conditions['itemType']=="1":
       accounts=search_account(conditions['account'],conditions['year'],conditions['month'])
       
       transaction_param=dict({"accountId":conditions['account']})
       if conditions['year']:
           transaction_param["transactionDate__year"]=conditions['year']
       
       if conditions['month']:
           transaction_param["transactionDate__month"]=conditions['month']
       
       transactions=get_transactions(transaction_param)
       
       return render_to_response('transactionBillManagement/searchAccount.html',locals())
           
    '''
        customer
    '''
    if conditions['itemType']=="2":
        accounts=search_customer(conditions['customer'],conditions['year'],conditions['month'])
        
        transaction_param=dict({"accountId":accounts[0][0]})
        transactions=get_transactions(transaction_param)
        
        return render_to_response('transactionBillManagement/searchCustomer.html',locals())
 

def accountBillList(request):

    accountId=get_currentId(request)
    
    transaction_param=dict({"accountId":accountId})
    transactions=get_transactions(transaction_param)
    #transactions=transactionBill.objects.filter(accountId=accountId)
    return render_to_response('transactionBillManagement/billList.html',locals())