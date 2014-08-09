# Create your views here.
from django.http import *
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
#from forms import addCustomerForm
from django.views.decorators.csrf import csrf_exempt
#from tables import customer
import string

# for test
#def hello(request):
#    return HttpResponse("Hello world")


@csrf_exempt
def messagesIndex(request):
    #customers = customer.objects.all()
    return render_to_response('messagesManagement/index.html')


def MessageForm(request):
    return render_to_response('messagesManagement/messageForm.html')
    #return HttpResponse("Hello world")