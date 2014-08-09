# coding=utf-8
# import os
# import sys
# print (os.getcwd() + '/../dataService2/')
from django.shortcuts import render_to_response
from django.shortcuts import redirect
from django.contrib import messages
from django.http import HttpResponse
from django.db import connection
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from osao import keystone
from osao import swift
from osao import nova
from osao import token as tokenApi
from dao import base as daobase
from dao import daozo
from hao import controller as hadoopController

def index(request):
    lName = request.session.get('name', False)
    if lName:
        return redirect('history/')
    else:
        return render_to_response('dp/index.html', locals(), RequestContext(request))

def tenant_select(request):
    lName = request.session.get('name', False)
    tName = request.session.get('tenant', False)
    token = request.session.get('token', False)
    if lName:
        master = daozo.getMasterOfAccount(lName)
        if tName and token:
            currentTenant = tName
            currentToken = token
        else:
            currrentTenant = None
            currentToken = None
        projectList = []
        res = daozo.getTenantList(lName)
        if master:
            for i in range(len(res)):
                url_s = '/dataProcessing/project/select/submit/?s=' + res[i][0]
                tenant = {
                          'name':res[i][0],
                          'role':res[i][1],
                          'desc':res[i][2],
                          'time':res[i][3],
                          'url_s':url_s,
                          }
                projectList.append(tenant)
        else:
            for i in range(len(res)):
                url_s = '/dataProcessing/project/select/submit/?s=' + res[i][0]
                tenant = {
                          'name':res[i][0],
                          'role':res[i][1],
                          'desc':res[i][2],
                          'time':res[i][3],
                          'url_s':url_s,
                          }
                projectList.append(tenant)
        return render_to_response('dp/project_select.html', locals(), RequestContext(request))
    else:
        messages.add_message(request, messages.WARNING, 'Please login first.', 'WARNING')
        return redirect('/login/')

def tenant_select_submit(request):
    lName = request.session.get('name', False)
    lPass = request.session.get('pass', False)
    if lName and lPass:
        tenant_name = request.GET['s']
        tenant_id = daobase.getTenantOSIDByName(tenant_name)
        token, mes = tokenApi.get_tenant_token(lName, lPass, tenant_id)
        request.session['tenant'] = tenant_name
        request.session['token'] = token
        currentTenant = tenant_name
        currentToken = token
        messages.add_message(request, messages.INFO, 'peoject changed', 'INFO')
        return redirect('/dataProcessing/project/select/')
    else:
        messages.add_message(request, messages.WARNING, 'Please login first.', 'WARNING')
        return redirect('/login/')
    
def data_process_history(request):
    lName = request.session.get('name', False)
    tName = request.session.get('tenant', False)
    token = request.session.get('token', False)
    if lName:
        if tName and token:
            dpList = daozo.data_processing_list(tName)
            return render_to_response('dp/process_history.html', locals(), RequestContext(request))
        else:
            messages.add_message(request, messages.ERROR, 'select your project.')
            return redirect('/dataProcessing/project/select/')
    else:
        messages.add_message(request, messages.WARNING, 'Please login first.', 'WARNING')
        return redirect('/login/')

def data_process_detail(request, id):
    lName = request.session.get('name', False)
    tName = request.session.get('tenant', False)
    token = request.session.get('token', False)
    if lName:
        if tName and token:
            detail = daozo.data_processing_detail(id)
            return render_to_response('dp/process_detail.html', locals(), RequestContext(request))
        else:
            messages.add_message(request, messages.ERROR, 'select your project.')
            return redirect('/dataProcessing/project/select/')
    else:
        messages.add_message(request, messages.WARNING, 'Please login first.', 'WARNING')
        return redirect('/login/')

def data_process_launch(request):
    lName = request.session.get('name', False)
    tName = request.session.get('tenant', False)
    token = request.session.get('token', False)
    if lName:
        if tName and token:
            files = request.session.get('col_cart', False)
            if files:
                fileList = files.split(';')
                fileList.remove('')
            else:
                fileList = []
            count = len(fileList)
            files = request.session.get('col_algo', False)
            if files:
                fileList = files.split(';')
                fileList.remove('')
            else:
                fileList = []
            counta = len(fileList)
            project = tName
            flavorList = nova.get_flavor_list(token, daobase.getTenantOSIDByName(tName))
            return render_to_response('dp/process_launch.html', locals(), RequestContext(request))
        else:
            messages.add_message(request, messages.ERROR, 'select your project.')
            return redirect('/dataProcessing/project/select/')
    else:
        messages.add_message(request, messages.WARNING, 'Please login first.', 'WARNING')
        return redirect('/login/')

@csrf_exempt
def data_process_launch_submit(request):
    lName = request.session.get('name', False)
    tName = request.session.get('tenant', False)
    token = request.session.get('token', False)
    if lName:
        if tName and token:
            files = request.session.get('col_cart', False)
            if files:
                fileList = files.split(';')
                fileList.remove('')
            else:
                fileList = []
            algos = request.session.get('col_algo', False)
            if algos:
                algoList = algos.split(';')
                algoList.remove('')
            else:
                algoList = []
            output = request.POST['processOutput']
            processName = request.POST['processName']
            image = "http://192.168.0.50:9292/v2/images/be5823fe-d2bd-4de1-af40-7d09733fab5c"
            flavorURL = "http://192.168.0.51:8774/v2/%s/flavor/%s" % (
                    daobase.getTenantOSIDByName(tName), request.POST['serverFlavor'])
            serverCount = request.POST['serverCount']
            serverLabel = request.POST['serverLabel']
            serverMeta = 'defaultServerMeta'
            hadoopMeta = 'defaultHadoopMeta'
            if(algos and files):
                flag = daozo.data_processing_launch(processName, tName, lName,
                    algos, files, output, serverLabel, int(serverCount),
                    flavorURL, serverMeta, hadoopMeta)
            else:
                messages.add_message(request, messages.ERROR, 'please check datas and algos.')
                flag = False
            if flag:
                processid = daobase.getDataProcessingIDByName(processName)
                hadoopController.hadoop(token, daobase.getTenantOSIDByName(tName), 
                                        processid, processName, int(serverCount),
                                        serverLabel, image, flavorURL, 
                                        files, algos, output,
                                        serverMeta, hadoopMeta)
                try:
                    del request.session['col_cart']
                    del request.session['col_algo']
                    messages.add_message(request, messages.SUCCESS,
                                         'data processing launch successful.')
                    return redirect('/dataProcessing/monitor/%s/' % (processid))
                except:
                    messages.add_message(request, messages.ERROR,
                                         'data processing launch failedddd.')
                    return redirect('/dataProcessing/launch/')
            else:
                count = len(fileList)
                counta = len(algoList)
                project = tName
                flavorList = nova.get_flavor_list(token, daobase.getTenantOSIDByName(tName))
                messages.add_message(request, messages.ERROR, 'something wrong.')
                return render_to_response('dp/process_launch.html',
                                          locals(), RequestContext(request))
        else:
            messages.add_message(request, messages.ERROR, 'select your project.')
            return redirect('/dataProcessing/project/select/')
    else:
        messages.add_message(request, messages.WARNING, 'Please login first.', 'WARNING')
        return redirect('/login/')

def data_collection_cart(request):
    lName = request.session.get('name', False)
    tName = request.session.get('tenant', False)
    token = request.session.get('token', False)
    if lName:
        if tName and token:
            files = request.session.get('col_cart', False)
            if files:
                fileList = files.split(';')
                fileList.remove('')
            else:
                fileList = []
            count = len(fileList)
            return render_to_response('dp/cart.html', locals(), RequestContext(request))
        else:
            messages.add_message(request, messages.ERROR, 'select your project.')
            return redirect('/dataProcessing/project/select/')
    else:
        messages.add_message(request, messages.WARNING, 'Please login first.', 'WARNING')
        return redirect('/login/')

def algorithm_cart(request):
    lName = request.session.get('name', False)
    tName = request.session.get('tenant', False)
    token = request.session.get('token', False)
    if lName:
        if tName and token:
            files = request.session.get('col_algo', False)
            if files:
                fileList = files.split(';')
                fileList.remove('')
            else:
                fileList = []
            count = len(fileList)
            return render_to_response('dp/carta.html', locals(), RequestContext(request))
        else:
            messages.add_message(request, messages.ERROR, 'select your project.')
            return redirect('/dataProcessing/project/select/')
    else:
        messages.add_message(request, messages.WARNING, 'Please login first.', 'WARNING')
        return redirect('/login/')

@csrf_exempt
def data_collection_add(request):
    lName = request.session.get('name', False)
    tName = request.session.get('tenant', False)
    token = request.session.get('token', False)
    if lName:
        if tName and token:
            if(request.method == 'POST'):
                container = request.POST['containerName']
                path = request.POST['filePath']
                fileName = request.POST['fileName']
                file_all = ''
                if path:
                    file_all = '%s/%s/%s' % (container, path , fileName)
                else:
                    file_all = '%s/%s' % (container, fileName)
                files = request.session.get('col_cart', False)
                if files:
                    request.session['col_cart'] = files + file_all + ';' 
                else:
                    request.session['col_cart'] = file_all + ';'
                messages.add_message(request, messages.SUCCESS,
                    'add %s to collection.' % file_all, 'SUCCESS')
            return redirect('/dataProcessing/collection/%s' % (container + '/' + path))
        else:
            messages.add_message(request, messages.ERROR, 'select your project.')
            return redirect('/dataProcessing/project/select/')
    else:
        messages.add_message(request, messages.WARNING, 'Please login first.', 'WARNING')
        return redirect('/login/')

@csrf_exempt
def algorithm_add(request):
    lName = request.session.get('name', False)
    tName = request.session.get('tenant', False)
    token = request.session.get('token', False)
    if lName:
        if tName and token:
            if(request.method == 'POST'):
                container = request.POST['containerName']
                path = request.POST['filePath']
                fileName = request.POST['fileName']
                file_all = ''
                if path:
                    file_all = '%s/%s/%s' % (container, path , fileName)
                else:
                    file_all = '%s/%s' % (container, fileName)
                files = request.session.get('col_algo', False)
                if files:
                    request.session['col_algo'] = files + file_all + ';' 
                else:
                    request.session['col_algo'] = file_all + ';'
                messages.add_message(request, messages.SUCCESS,
                    'add %s to collection.' % file_all, 'SUCCESS')
            return redirect('/dataProcessing/algorithm/%s' % (container + '/' + path))
        else:
            messages.add_message(request, messages.ERROR, 'select your project.')
            return redirect('/dataProcessing/project/select/')
    else:
        messages.add_message(request, messages.WARNING, 'Please login first.', 'WARNING')
        return redirect('/login/')

@csrf_exempt
def data_collection_del(request):
    lName = request.session.get('name', False)
    tName = request.session.get('tenant', False)
    token = request.session.get('token', False)
    if lName:
        if tName and token:
            if(request.method == 'POST'):
                file = request.POST['file']
                files = request.session.get('col_cart', False)
                if files:
                    files = files[:files.find(file)] + files[files.find(file) + len(file) + 1:]
                else:
                    pass
                request.session['col_cart'] = files
                messages.add_message(request, messages.SUCCESS,
                    'del %s from collection.' % file, 'SUCCESS')
            return redirect('/dataProcessing/collection/cart/')
        else:
            messages.add_message(request, messages.ERROR, 'select your project.')
            return redirect('/dataProcessing/project/select/')
    else:
        messages.add_message(request, messages.WARNING, 'Please login first.', 'WARNING')
        return redirect('/login/')

@csrf_exempt
def algorithm_del(request):
    lName = request.session.get('name', False)
    tName = request.session.get('tenant', False)
    token = request.session.get('token', False)
    if lName:
        if tName and token:
            if(request.method == 'POST'):
                file = request.POST['file']
                files = request.session.get('col_algo', False)
                if files:
                    files = files[:files.find(file)] + files[files.find(file) + len(file) + 1:]
                else:
                    pass
                request.session['col_algo'] = files
                messages.add_message(request, messages.SUCCESS,
                    'del %s from collection.' % file, 'SUCCESS')
            return redirect('/dataProcessing/algorithm/cart/')
        else:
            messages.add_message(request, messages.ERROR, 'select your project.')
            return redirect('/dataProcessing/project/select/')
    else:
        messages.add_message(request, messages.WARNING, 'Please login first.', 'WARNING')
        return redirect('/login/')

def data_collection_clear(request):
    lName = request.session.get('name', False)
    tName = request.session.get('tenant', False)
    token = request.session.get('token', False)
    if lName:
        if tName and token:
            try:
                del request.session['col_cart']
            except:
                messages.add_message(request, messages.ERROR, 'collection clear failed.', 'ERROR')
            else:
                messages.add_message(request, messages.SUCCESS, 'collection cleared.', 'SUCCESS')
            return redirect('/dataProcessing/algorithm/cart/')
        else:
            messages.add_message(request, messages.ERROR, 'select your project.')
            return redirect('/dataProcessing/project/select/')
    else:
        messages.add_message(request, messages.WARNING, 'Please login first.', 'WARNING')
        return redirect('/login/')

def algorithm_clear(request):
    lName = request.session.get('name', False)
    tName = request.session.get('tenant', False)
    token = request.session.get('token', False)
    if lName:
        if tName and token:
            try:
                del request.session['col_algo']
            except:
                messages.add_message(request, messages.ERROR, 'collection clear failed.', 'ERROR')
            else:
                messages.add_message(request, messages.SUCCESS, 'collection cleared.', 'SUCCESS')
            return redirect('/dataProcessing/algorithm/cart/')
        else:
            messages.add_message(request, messages.ERROR, 'select your project.')
            return redirect('/dataProcessing/project/select/')
    else:
        messages.add_message(request, messages.WARNING, 'Please login first.', 'WARNING')
        return redirect('/login/')

def data_collection_set(request):
    lName = request.session.get('name', False)
    tName = request.session.get('tenant', False)
    token = request.session.get('token', False)
    if lName:
        if tName and token:
            container_list = swift.get_containerList(token,
                daobase.getTenantOSIDByName(tName))
            files = request.session.get('col_cart', False)
            if files:
                fileList = files.split(';')
                fileList.remove('')
            else:
                fileList = []
            count = len(fileList)
            return render_to_response('dp/collection_container_select.html', locals(), RequestContext(request))
        else:
            messages.add_message(request, messages.ERROR, 'select your project.')
            return redirect('/dataProcessing/project/select/')
    else:
        messages.add_message(request, messages.WARNING, 'Please login first.', 'WARNING')
        return redirect('/login/')

def algorithm_set(request):
    lName = request.session.get('name', False)
    tName = request.session.get('tenant', False)
    token = request.session.get('token', False)
    if lName:
        if tName and token:
            container_list = swift.get_containerList(token,
                daobase.getTenantOSIDByName(tName))
            algos = request.session.get('col_algo', False)
            if algos:
                fileList = algos.split(';')
                fileList.remove('')
            else:
                fileList = []
            count = len(fileList)
            return render_to_response('dp/collection_container_selecta.html', locals(), RequestContext(request))
        else:
            messages.add_message(request, messages.ERROR, 'select your project.')
            return redirect('/dataProcessing/project/select/')
    else:
        messages.add_message(request, messages.WARNING, 'Please login first.', 'WARNING')
        return redirect('/login/')

def container_select(request, path):
    lName = request.session.get('name', False)
    tName = request.session.get('tenant', False)
    token = request.session.get('token', False)
    if lName:
        if tName and token:
            current_path = path + '/'
            temp = path + '/'
            parrent_path = []
            while(temp.find('/') > -1):
                if(len(parrent_path) > 0):
                    parrent_path.append({'k':parrent_path[len(parrent_path) - 1]['k'] + 
                                          temp[:temp.find('/') + 1],
                                         'v':temp[:temp.find('/')]})
                else:
                    parrent_path.append({'k':'/dataProcessing/collection/' + 
                                         current_path[:current_path.find('/') + 1],
                                         'v':temp[:temp.find('/')]})
                # print parrent_path
                temp = temp[temp.find('/') + 1:]
                # print temp
            # print path
            i = path.find('/')
            if(i > -1):
                container_name = path[:i]
                path = path[i + 1:]
            else:
                container_name = path
                path = ''
            # print container_name
            # print path
            files = request.session.get('col_cart', False)
            if files:
                fileList = files.split(';')
                fileList.remove('')
            else:
                fileList = []
            count = len(fileList)
            folder_list, file_list, = swift.get_fileList(token,
                daobase.getTenantOSIDByName(tName), container_name, path)
            container_list = swift.get_containerList(token,
                daobase.getTenantOSIDByName(tName))
            container_metadata = swift.get_ContainerMetadata(token,
                daobase.getTenantOSIDByName(tName), container_name)
            return render_to_response('dp/collection_file_select.html', locals(), RequestContext(request))
        else:
            messages.add_message(request, messages.ERROR, 'select your project.')
            return redirect('/virtualHost/project/select/')
    else:
        messages.add_message(request, messages.WARNING, 'Please login first.', 'WARNING')
        return redirect('/login/')

def algorithm_select(request, path):
    lName = request.session.get('name', False)
    tName = request.session.get('tenant', False)
    token = request.session.get('token', False)
    if lName:
        if tName and token:
            current_path = path + '/'
            temp = path + '/'
            parrent_path = []
            while(temp.find('/') > -1):
                if(len(parrent_path) > 0):
                    parrent_path.append({'k':parrent_path[len(parrent_path) - 1]['k'] + 
                                          temp[:temp.find('/') + 1],
                                         'v':temp[:temp.find('/')]})
                else:
                    parrent_path.append({'k':'/dataProcessing/algorithm/' + 
                                         current_path[:current_path.find('/') + 1],
                                         'v':temp[:temp.find('/')]})
                # print parrent_path
                temp = temp[temp.find('/') + 1:]
                # print temp
            # print path
            i = path.find('/')
            if(i > -1):
                container_name = path[:i]
                path = path[i + 1:]
            else:
                container_name = path
                path = ''
            # print container_name
            # print path
            files = request.session.get('col_algo', False)
            if files:
                fileList = files.split(';')
                fileList.remove('')
            else:
                fileList = []
            count = len(fileList)
            folder_list, file_list, = swift.get_fileList(token,
                daobase.getTenantOSIDByName(tName), container_name, path)
            container_list = swift.get_containerList(token,
                daobase.getTenantOSIDByName(tName))
            container_metadata = swift.get_ContainerMetadata(token,
                daobase.getTenantOSIDByName(tName), container_name)
            return render_to_response('dp/collection_file_selecta.html', locals(), RequestContext(request))
        else:
            messages.add_message(request, messages.ERROR, 'select your project.')
            return redirect('/virtualHost/project/select/')
    else:
        messages.add_message(request, messages.WARNING, 'Please login first.', 'WARNING')
        return redirect('/login/')

def data_process_monitor(request, id):
    lName = request.session.get('name', False)
    tName = request.session.get('tenant', False)
    token = request.session.get('token', False)
    if lName:
        if tName and token:
            if int(id) < 1:
                messages.add_message(request, messages.ERROR, 'select a data processing.')
                return redirect('/dataProcessing/history/')
            else:
                dpid = id
                return render_to_response('dp/process_monitor.html', locals(), RequestContext(request))
        else:
            messages.add_message(request, messages.ERROR, 'select your project.')
            return redirect('/dataProcessing/project/select/')
    else:
        messages.add_message(request, messages.WARNING, 'Please login first.', 'WARNING')
        return redirect('/login/')

def data_process_status(request, id):
    lName = request.session.get('name', False)
    tName = request.session.get('tenant', False)
    token = request.session.get('token', False)
    if lName:
        if tName and token:
            dpDetail = daozo.data_processing_detail(id)
            try:
                status = dpDetail['status']
            except:
                messages.add_message(request, messages.ERROR, 'select a data processing.')
                return redirect('/dataProcessing/history/')
            else:
                if status == 'building':
                    serverList = nova.server_list(token, daobase.getTenantOSIDByName(tName))
                    for s in serverList:
                        if s['name'].find(daobase.getDataProcessingServerNameByID(int(id)))>-1:
                            s.setdefault('flavorInfo', nova.flavor_detail(token,
                                        daobase.getTenantOSIDByName(tName), s['flavor']['id']))
                        else:
                            serverList.remove(s)                        
                    return render_to_response('dp/_step_building.html',
                                          locals(), RequestContext(request))
                if status == 'setting':
                    return render_to_response('dp/_step_setting.html',
                                          locals(), RequestContext(request))
                if status == 'running':
                    return render_to_response('dp/_step_running.html',
                                          locals(), RequestContext(request))
                if status == 'releasing':
                    return render_to_response('dp/_step_releasing.html',
                                          locals(), RequestContext(request))
        else:
            messages.add_message(request, messages.ERROR, 'select your project.')
            return redirect('/dataProcessing/project/select/')
    else:
        messages.add_message(request, messages.WARNING, 'Please login first.', 'WARNING')
        return redirect('/login/')
