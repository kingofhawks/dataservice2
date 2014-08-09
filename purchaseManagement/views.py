# Create your views here.
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_exempt
from db.api.purchase import *


@csrf_exempt
def transactionIndex(request):
    purchaseProducts=list_purchaseProducts()
    purchasePackages=list_purchasePackages()
    
    return render_to_response('purchaseManagement/transactionsIndex.html',locals())

@csrf_exempt
def search(request):
    
    condition={}
    
    conditions=get_searchConditions(request)
    
    if conditions['productType'] in ["0","1"]:
        purchaseProducts=search_purchaseProducts(conditions)
    
    if conditions['productType'] in ["0","2"]:
        purchasePackages=search_purchasePackages(conditions)
    
    return render_to_response('purchaseManagement/search.html',locals())
    