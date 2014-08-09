#coding=utf-8
# Create your views here.
from django.http import *
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_exempt
from db.api.login import login_auth
from django.contrib import messages
from django.template import *



#from django.contrib.auth import authenticate,login,logout

def index(request):
    name = request.session.get('admin',False)
  #  pwd = request.session.get('password')
    
    
    return render_to_response('login/login.html',locals(),context_instance=RequestContext(request))

@csrf_exempt
def login(request):
    if login_auth(request.POST['user'],request.POST['pwd'])=="1":
        '''the user does not exist '''
        messageStr=request.POST['user']+" does not exist."
        messages.add_message(request,messages.ERROR,messageStr)
        #return render_to_response('login/login.html',locals(),context_instance=RequestContext(request))
        return HttpResponseRedirect(reverse("login.views.index"))  
    elif login_auth(request.POST['user'],request.POST['pwd'])=="2":
        '''login '''     
        request.session['admin'] = request.POST['user']
        #request.session['password'] = request.POST['pwd']
        
        return HttpResponseRedirect(reverse("login.views.framset"))
    elif login_auth(request.POST['user'],request.POST['pwd'])=="3":
        '''Wrong name or password '''
        messages.add_message(request,messages.ERROR,"Wrong name or password")
        return HttpResponseRedirect(reverse("login.views.index"))
        #html="<html><body>user:%s,pwd:%s</body></html>" %(request.POST['user'],request.POST['pwd'])
        #return HttpResponse(html)
    
def logout(request):
    try:
        del request.session['admin']        
    except KeyError:
        pass
    return render_to_response('login/login.html',locals(),context_instance=RequestContext(request))

def framset(request):    
    return render_to_response('login/index.html')

def navigation(request):
    name = request.session.get('admin', False)
       
    return render_to_response('login/left.html',locals())