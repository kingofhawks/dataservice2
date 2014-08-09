# coding=utf-8
import os
import sys
from django.shortcuts import render_to_response
from django.shortcuts import redirect
from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.db import connection
from django.db import transaction
from dao import daozo
from osao import keystone
from models import Data
from tables import DataTable
from django_tables2   import RequestConfig
from forms import UploadFileForm
from forms import DataTradeForm
from django.core.context_processors import csrf
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from django.core.servers.basehttp import FileWrapper
from swiftclient import client as c    
import mimetypes


def index(request):
    name = lName = request.session.get('name', False)
    if lName:
        vhList = []
        vhList.append('dtind')
    return render_to_response('dt/index.html', locals())

def data_list(request):
    #name = lName = request.session.get('name', False)
    lName = request.session.get('name', False)
    print '***********'+str(lName)
    if lName:
        vhList = []
        vhList.append('dtind')
    table = DataTable(Data.objects.all())
    RequestConfig(request, paginate={"per_page": 25}).configure(table)
    return render(request, 'dt/data_list.html', {'table': table,'lName':lName})

#@csrf_exempt
def publish(request):
    name = lName = request.session.get('name', False)
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        #print form.errors
        if form.is_valid():  
            handle_uploaded_file(request)
            title = request.POST.get('title')
            description = request.POST.get('description')
            price = request.POST.get('price')
            category = request.POST.get('category')
            #print request.POST.get('title')
            from datetime import date
            data = Data(title=title,description=description,price=price,category=category,creator=request.session.get('name'),createdDate=date.today())
            data.save()
            
            return HttpResponseRedirect('/market/mypublish/')
        else:
            return HttpResponse(form)
    else:
        form = UploadFileForm()
        return render_to_response('dt/publish.html', {'form': form,'lName':lName},context_instance=RequestContext(request))
    
def my_publish(request):
    name = lName = request.session.get('name', False)
    if lName:
        vhList = []
        vhList.append('dtind')
    table = DataTable(Data.objects.filter(creator=request.session.get('name')))
    RequestConfig(request, paginate={"per_page": 25}).configure(table)
    return render(request, 'dt/my_publish.html', {'table': table,'lName':lName})

def handle_uploaded_file(request):
    f = request.FILES['file']
#     with open('E:/sample.txt', 'wb+') as destination:
#         for chunk in f.chunks():
#             destination.write(chunk)
    token = request.session.get('token')
    tenant_id = request.session.get('tenant_id')
    print 'token:%s***tenant:%s' %(token,tenant_id)
    url='http://192.168.0.55:8888/v1/AUTH_'+str(tenant_id)
    container = 'Publish'
    containers = c.get_account(url,token)[1]
    print containers
    if get_container(containers,container):
        pass
    else:
        print 'put container %s' %(container)
        c.put_container(url,token,container)     
    c.put_object(url,token,container,name=f.name,contents=f)    
            
def my_data(request):
    name = lName = request.session.get('name', False)
    if lName:
        vhList = []
        vhList.append('dtind')
        #select * from dt_data d where d.id in (select da.data_id from dt_data_account da where da.account_id=7)
    #table = DataTable(Data.objects.filter(creator=request.session.get('name')))
    user_id = request.session.get('user_id')
    table = DataTable(Data.objects.extra(where=["dt_data.id in (select da.data_id from dt_data_account da where da.account_id=%s)"],params=[user_id]))
    RequestConfig(request, paginate={"per_page": 25}).configure(table)
    
    cursor = connection.cursor()
    cursor.execute("SELECT apikey FROM t_account WHERE loginName = %s", [name])
    row = cursor.fetchone()
    #print row
    
    return render(request, 'dt/my_subsription.html', {'table': table,'lName':lName,'key':row[0]})


def data_detail(request,pk):
#     if request.method == 'POST':
#         return subsribe(request,pk)
    name = lName = request.session.get('name', False)
    if lName:
        vhList = []
        vhList.append('dtind')
    data = Data.objects.get(id=pk)
    print data
    request.session['data_id'] = pk
    return render(request, 'dt/data_detail.html', {'data': data,'lName':lName})

@transaction.commit_manually
def subsribe(request,pk):
    user_id = request.session.get('user_id')
    print str(user_id)+'***********'+str(pk)
    sql = '''insert into dt_data_account(data_id,account_id) values ('%s','%s') ''' % (
        pk, user_id)
    cursor = connection.cursor()
    cursor.execute(sql)
    transaction.commit()
    return HttpResponseRedirect('/market/mydata/')

def data_trade(request):
    name = lName = request.session.get('name', False)
    if request.method == 'POST':
        form = DataTradeForm(request.POST)
        if form.is_valid():    
            pk = request.session.get('data_id',False)        
            return subsribe(request,pk)          
    else:
        form = DataTradeForm(initial={'payment': '1'})
        return render_to_response('dt/data_trade.html', {'form': form,'lName':lName},context_instance=RequestContext(request))


def upload(request):
    form = UploadFileForm()
    return render_to_response('contact.html', {'form': form})

def download(request):
    '''
    download data to local PC
    '''
    try:
        #TODO
        file_name = 'E:/sample.docx'
        fsock = open(file_name,"r")
        mime_type_guess = mimetypes.guess_type(file_name)
        if mime_type_guess is not None:
            response = HttpResponse(fsock, mimetype=mime_type_guess[0])  
        response['Content-Length'] = os.path.getsize(file_name)         
        response['Content-Disposition'] = 'attachment; filename=' + file_name 
        #response['X-Sendfile'] = file_name
        print 'succeed download file'           
    except IOError:
        response = HttpResponseNotFound()
    return response

def download_cloudstorage(request):
    '''
    download data to cloud storage
    '''
    token = request.session.get('token')
    tenant_id = request.session.get('tenant_id')
    print 'token:%s***tenant:%s' %(token,tenant_id)
    #url='http://192.168.0.55:8888/v1/AUTH_93e0ff98ddfb4bb28d936c049a89714b'
    url='http://192.168.0.55:8888/v1/AUTH_'+str(tenant_id)
    container = 'Subscriptions'
    containers = c.get_account(url,token)[1]
    print containers
    if get_container(containers,container):
        pass
    else:
        print 'put container %s' %(container)
        c.put_container(url,token,container)     
    #TODO
    c.put_object(url,token,container,name='test222',contents='test')
    return HttpResponse('ok')

def get_container(containers,container):
    for c in containers:
        if c['name'] == container:
            return c
    return None

@transaction.commit_manually
def api_key(request):
    from django.utils import simplejson
    import uuid
    import hmac
    
    try:
        from hashlib import sha1
    except ImportError:
        import sha
        sha1 = sha.sha
    
    new_uuid = uuid.uuid4()
    key = hmac.new(str(new_uuid), digestmod=sha1).hexdigest()
    name = request.session.get('name', False)
    
    sql = '''update t_account set apikey= '%s' where loginName = '%s' ''' % (
        key, name)
    cursor = connection.cursor()
    cursor.execute(sql)
    transaction.commit()
    
    data = {
       'key': key,       
    }
    
    return HttpResponse(simplejson.dumps(data), mimetype='application/json')