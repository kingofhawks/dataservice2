# coding=utf-8
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template.loader import get_template
from django.template import Context
from django.template import RequestContext
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.db import transaction
from django.db import connection
import MySQLdb
import logging
from dao import daozo
# from bean import customer

def index(request):
    lName = request.session.get('name', False)
    return render_to_response('index.html', locals())

def login(request):
    lName = request.session.get('name', False)
    if lName:
        pass
    else:
        messages.add_message(request, messages.WARNING, 'Enter your name and password', 'WARNING')
    return render_to_response('login.html', locals(), RequestContext(request))

@csrf_exempt
def login_submit(request):
    if request.method == 'POST':
        res = daozo.get_account(request.POST['loginName'], request.POST['pass'])
        if(len(res) > 1):
            logging.getLogger('operate').log(50, 'LOGIN POST %s %s,system error!.' % 
            (request.POST['loginName'], request.POST['pass']))
            return HttpResponse('ERROR')
        if(len(res) < 1):
            messages.add_message(request, messages.ERROR, 'Wrong name or password.')
            logging.getLogger('operate').log(30, 'LOGIN %s %s faild .' % 
            (request.POST['loginName'], request.POST['pass']))
            # return render_to_response('login.html', locals())
            return render_to_response('login.html', locals(), RequestContext(request))
        request.session['name'] = res[0][0]
        request.session['pass'] = request.POST['pass']
        request.session['user_id']=res[0][1]
        
        logging.getLogger('operate').log(20, 'LOGIN %s success.' % request.POST['loginName'])
        messages.add_message(request, messages.INFO, 'login successful.')
    return redirect('/my/')

def regist(request):
    lName = request.session.get('name', False)
    messages.add_message(request, messages.INFO, 'Enter your info') 
    return render_to_response('regist.html', locals(), RequestContext(request))

@csrf_exempt
def regist_submit(request):
    if request.method == 'POST':
        # one = customer.Customer()
        # one.set_lle(request.POST['loginName'], request.POST['password1'], request.POST['email'])
        logging.getLogger('operate').log(20, 'get regist post %s %s %s.' % 
        (request.POST['loginName'], request.POST['password1'], request.POST['email']))
        flag = daozo.account_regist(request.POST['loginName'], request.POST['password1'], request.POST['email'])
        if(flag):
            request.session['name'] = request.POST['loginName']
            logging.getLogger('operate').log(20, 'REGIST %s %s %s successed and logined in.' % 
            (request.POST['loginName'], request.POST['password1'], request.POST['email']))
            return redirect('/login/')
        else :
            logging.getLogger('operate').log(30, 'REGIST %s %s %s failed.' % 
            (request.POST['loginName'], request.POST['password1'], request.POST['email']))
            messages.add_message(request, messages.ERROR, 'Registration failed.')
    return render_to_response('regist.html', locals(), RequestContext(request)) 

def regist_loginName_check(request):
    r = daozo.check_regist_loginName(request.GET['n'])
    return HttpResponse(len(r))

def regist_email_check(request):
    r = daozo.check_regist_loginName(request.GET['e'])
    return HttpResponse(len(r))

def logout(request):
    try:
        logging.getLogger('operate').log(20, 'LOGOUT %s.' % request.session['name'])
        del request.session['name']
        del request.session['tenant']
        del request.session['token']
    except KeyError:
        pass
    return redirect('/')

# deprecated
# def virtualHost(request):
    # if request.session.get('name', False):
        # name = request.session['name']
    # return render_to_response('virtualHost.html', locals())

# deprecated
# def cloudStorage(request):
    # if request.session.get('name', False):
        # name = request.session['name']
    # return render_to_response('cloudStorage.html', locals())

# deprecated
# def dataProcessing(request):
#    if request.session.get('name', False):
#        lName = request.session['name']
#    return render_to_response('dataProcessing.html', locals())

# deprecated
# def dataTrade(request):
#    if request.session.get('name', False):
#        lName = request.session['name']
#    return render_to_response('dataTrade.html', locals())

# deprecated
# def pricingStandrd(request):
#    if request.session.get('name', False):
#        lName = request.session['name']
#    return render_to_response('pricingStandrd.html', locals())

# deprecated
# def supportCenter(request):
#    if request.session.get('name', False):
#        lName = request.session['name']
#    return render_to_response('supportCenter.html', locals())
