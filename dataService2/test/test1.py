# coding=utf-8
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template.loader import get_template
from django.template import Context
from django.contrib import messages
from django.db import connection
from django.template import RequestContext
import datetime
import time

def hello(requset):
    return HttpResponse('hello,i\'m running!#coding=utf-8,哈哈')

def hello2(request):
    time = datetime.datetime.now()
    message = 'start running'
    t = get_template('hello/hello2.html')
    html = t.render(Context({'t': time}))
    return HttpResponse(html)

def hello3(request):
    time = datetime.datetime.now()
    return render_to_response('hello/hello2.html', {'t': time})

def tuisuan(dwjz0, dwjzn, gmje, sgfl, shfl):
    jsgje = gmje / (1 + sgfl)
    fe = jsgje / dwjz0
    sgfy = gmje - jsgje
    shze = fe * dwjzn
    shfy = shze * shfl
    shje = shze - shfy   
    zsy = shje - shfy
    jg = {
            'gmje':gmje,
            'sgjg':dwjz0,
            'sgfy':sgfy,
            'gmfe':fe,
            'shsd':shje,
            'shjg':dwjzn,
            'shfy':shfy,
            'shfe':fe,
            'sy':zsy,
       }
    return jg

def hello4(request):
    t = datetime.datetime.now()
    m = 'cal'
#    dwjz0=1.0
#    dwjzn=1.0
#    sgfl=1.5/100
#    shfl=0.5/100
#    jg=tuisuan(1.2,2.1,1000,1.5/100,0.5/100)
    return render_to_response('hello/hello3.html', locals())

def hello5(request):
#    db = MySQLdb.connect(user='me', db='mydb', passwd='secret', host='localhost')
#    cursor = db.cursor()
    connection.queries
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM customer')
    accounts = cursor.fetchall()
    p = {'SN':11, 'LoginName':'abc', 'LoginPass':'def', 'User':'no name', 'Status':1}
    accList = [p, ]
    for i in range(len(accounts)):
        new = {
             'SN':accounts[i][0],
             'LoginName':accounts[i][1],
             'LoginPass':accounts[i][2],
             'User':accounts[i][3],
             'Status':accounts[i][4]
            }
        accList.append(new)
    request_path = "welecome to the page at %s" % request.path
    ua = request.META.get('HTTP_USER_AGENT', 'unknown')
    meta_values = request.META.items()
    return render_to_response('hello/hello5.html', locals())

def hello6(request):
    temp = 'this is test'
    request.session['name'] = 'testName'
    testName = request.session.get('name', False)
    messages.add_message(request, messages.ERROR, 'Hello world.')
    # return render_to_response('hello/hello6.html', locals())
    return render_to_response('hello/hello6.html', locals(), context_instance=RequestContext(request))
    
def searchtest(request):
    if 'q' in request.GET:
        message = 'You searched for: %r' % request.GET['q']
    else:
        message = 'You submitted an empty form.'
    return HttpResponse(message)

def contacttest(request):
    errors = []
    if request.method == 'POST':
        if not request.POST.get('subject', ''):
            errors.append('Enter a subject.')
        if not request.POST.get('message', ''):
            errors.append('Enter a message.')
        if request.POST.get('email') and '@' not in request.POST['email']:
            errors.append('Enter a valid e-mail address.')
        if not errors:
            errors.append(request.POST.get('subject', ''))
            errors.append(request.POST.get('message', ''))
            errors.append(request.POST.get('email', ''))
#            send_mail(
#                request.POST['subject'],
#                request.POST['message'],
#                request.POST.get('email', 'noreply@example.com'),
#                ['siteowner@example.com'],
#            )
    return HttpResponse(errors)
#
#
#
#
#
