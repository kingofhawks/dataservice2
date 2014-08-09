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
from django.core.context_processors import csrf 
from dao import daozo
from dao import base as daobase
from osao import keystone
from osao import swift
from osao import token as tokenApi

def index(request):
    lName = request.session.get('name', False)
    tName = request.session.get('tenant', False)
    token = request.session.get('token', False)
    if lName:
        if tName and token:
            return redirect('/cloudStorage/display/')
        else:
            return redirect('/cloudStorage/project/select/')
    else:
        return render_to_response('cs/index.html', locals(), RequestContext(request))

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
                url_s = '/cloudStorage/project/select/submit/?s=' + res[i][0]
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
                url_s = '/cloudStorage/project/select/submit/?s=' + res[i][0]
                tenant = {
                          'name':res[i][0],
                          'role':res[i][1],
                          'desc':res[i][2],
                          'time':res[i][3],
                          'url_s':url_s,
                          }
                projectList.append(tenant)
        metadata = swift.get_metadata(token, daobase.getTenantOSIDByName(tName))
        container_list = swift.get_containerList(token, daobase.getTenantOSIDByName(tName))
        return render_to_response('cs/project_select.html', locals(), RequestContext(request))
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
        return redirect('/cloudStorage/project/select/')
    else:
        messages.add_message(request, messages.WARNING, 'Please login first.', 'WARNING')
        return redirect('/login/')

def displsy(request):
    lName = request.session.get('name', False)
    tName = request.session.get('tenant', False)
    token = request.session.get('token', False)
    if lName:
        if tName and token:
            metadata = swift.get_metadata(token, daobase.getTenantOSIDByName(tName))
            container_list = swift.get_containerList(token, daobase.getTenantOSIDByName(tName))
            return render_to_response('cs/display.html', locals(), RequestContext(request))
        else:
            messages.add_message(request, messages.ERROR, 'select your project.')
            return redirect('/cloudStorage/project/select/')
    else:
        messages.add_message(request, messages.WARNING, 'Please login first.', 'WARNING')
        return redirect('/login/')

def container(request, path):
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
                    parrent_path.append({'k':'/cloudStorage/display/' + 
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
            folder_list, file_list, = swift.get_fileList(token,
                daobase.getTenantOSIDByName(tName), container_name, path)
            container_list = swift.get_containerList(token,
                daobase.getTenantOSIDByName(tName))
            container_metadata = swift.get_ContainerMetadata(token,
                daobase.getTenantOSIDByName(tName), container_name)
            return render_to_response('cs/display_container.html', locals(), RequestContext(request))
        else:
            messages.add_message(request, messages.ERROR, 'select your project.')
            return redirect('/cloudStorage/project/select/')
    else:
        messages.add_message(request, messages.WARNING, 'Please login first.', 'WARNING')
        return redirect('/login/')

def container_create(request):
    lName = request.session.get('name', False)
    tName = request.session.get('tenant', False)
    token = request.session.get('token', False)
    if lName:
        if tName and token:
            metadata = swift.get_metadata(token, daobase.getTenantOSIDByName(tName))
            container_list = swift.get_containerList(token, daobase.getTenantOSIDByName(tName))
            return render_to_response('cs/container_create.html', locals(), RequestContext(request))
        else:
            messages.add_message(request, messages.ERROR, 'select your project.')
            return redirect('/cloudStorage/project/select/')
    else:
        messages.add_message(request, messages.WARNING, 'Please login first.', 'WARNING')
        return redirect('/login/')

@csrf_exempt
def container_create_submit(request):
    lName = request.session.get('name', False)
    tName = request.session.get('tenant', False)
    token = request.session.get('token', False)
    if lName:
        if tName and token:
            status, reason = swift.container_create(token,
                daobase.getTenantOSIDByName(tName), request.POST['containerName'])
            messages.add_message(request, messages.INFO, status, 'INFO')
            messages.add_message(request, messages.INFO, reason, 'INFO')
            return redirect('/cloudStorage/')
        else:
            messages.add_message(request, messages.ERROR, 'select your project.')
            return redirect('/cloudStorage/project/select/')
    else:
        messages.add_message(request, messages.WARNING, 'Please login first.', 'WARNING')
        return redirect('/login/')
    
@csrf_exempt
def container_delete_submit(request):
    lName = request.session.get('name', False)
    tName = request.session.get('tenant', False)
    token = request.session.get('token', False)
    if lName:
        if tName and token:
            if(request.method == 'POST'):
                status, reason = swift.container_delete(token, daobase.getTenantOSIDByName(tName),
                    request.POST['containerName'])
                if(status == 204):
                    messages.add_message(request, messages.SUCCESS, status, 'SUCCESS')
                    messages.add_message(request, messages.SUCCESS, 'delete successful', 'SUCCESS')
                else:
                    messages.add_message(request, messages.ERROR, status, 'ERROR')
                    messages.add_message(request, messages.ERROR, reason, 'ERROR')
            return redirect('/cloudStorage/')
        else:
            messages.add_message(request, messages.ERROR, 'select your project.')
            return redirect('/cloudStorage/project/select/')
    else:
        messages.add_message(request, messages.WARNING, 'Please login first.', 'WARNING')
        return redirect('/login/')

def folder_create(request):
    lName = request.session.get('name', False)
    tName = request.session.get('tenant', False)
    token = request.session.get('token', False)
    if lName:
        if tName and token:
            path = request.GET['p']
            i = path.find('/')
            if(i > -1):
                container_name = path[:i]
            else:
                container_name = path
            container_list = swift.get_containerList(token,
                daobase.getTenantOSIDByName(tName))
            container_metadata = swift.get_ContainerMetadata(token,
                daobase.getTenantOSIDByName(tName), container_name)
            return render_to_response('cs/folder_create.html', locals(), RequestContext(request))
        else:
            messages.add_message(request, messages.ERROR, 'select your project.')
            return redirect('/cloudStorage/project/select/')
    else:
        messages.add_message(request, messages.WARNING, 'Please login first.', 'WARNING')
        return redirect('/login/')

@csrf_exempt
def folder_create_submit(request):
    lName = request.session.get('name', False)
    tName = request.session.get('tenant', False)
    token = request.session.get('token', False)
    if lName:
        if tName and token:
            if request.method == 'POST':
                container = request.POST['container']
                path = request.POST['folderPath']
                folder_full = path[len(container) + 1:] + request.POST['folderName']
                # print type(folder_full)
                # print folder_full
                status, reason = swift.folder_create(token, daobase.getTenantOSIDByName(tName),
                    container, folder_full)
                if status == 201:
                    messages.add_message(request, messages.SUCCESS, status, 'SUCCESS')
                    messages.add_message(request, messages.SUCCESS, reason, 'SUCCESS')
                else:
                    messages.add_message(request, messages.ERROR, status, 'ERROR')
                    messages.add_message(request, messages.ERROR, reason, 'ERROR')
            return redirect('/cloudStorage/display/%s' % (path))
        else:
            messages.add_message(request, messages.ERROR, 'select your project.')
            return redirect('/cloudStorage/project/select/')
    else:
        messages.add_message(request, messages.WARNING, 'Please login first.', 'WARNING')
        return redirect('/login/')

@csrf_exempt
def folder_delete_submit(request):
    lName = request.session.get('name', False)
    tName = request.session.get('tenant', False)
    token = request.session.get('token', False)
    if lName:
        if tName and token:
            if(request.method == 'POST'):
                container = request.POST['containerName']
                path = request.POST['folderPath']
                if path:
                    folder_all = request.POST['folderPath'] + '/' + request.POST['folderName']
                else:
                    folder_all = request.POST['folderName']
                l1, l2 = swift.get_fileList(token, daobase.getTenantOSIDByName(tName), container, folder_all)
                if (len(l1) + len(l2)) > 0:
                    status = 404
                    reason = 'not empty'
                else:
                    status, reason = swift.folder_delete(token, daobase.getTenantOSIDByName(tName),
                    container, folder_all)
                if(status == 204):
                    messages.add_message(request, messages.SUCCESS, status, 'SUCCESS')
                    messages.add_message(request, messages.SUCCESS, 'delete successful', 'SUCCESS')
                else:
                    messages.add_message(request, messages.ERROR, status, 'ERROR')
                    messages.add_message(request, messages.ERROR, reason, 'ERROR')
                return redirect('/cloudStorage/display/%s' % (container + '/' + path))
            else:
                return redirect('/cloudStorage/')
        else:
            messages.add_message(request, messages.ERROR, 'select your project.')
            return redirect('/cloudStorage/project/select/')
    else:
        messages.add_message(request, messages.WARNING, 'Please login first.', 'WARNING')
        return redirect('/login/')

@csrf_exempt
def file_delete_submit(request):
    lName = request.session.get('name', False)
    tName = request.session.get('tenant', False)
    token = request.session.get('token', False)
    if lName:
        if tName and token:
            if(request.method == 'POST'):
                container = request.POST['containerName']
                path = request.POST['filePath']
                file_all = ''
                if path:
                    file_all = path + '/' + request.POST['fileName']
                else:
                    file_all = request.POST['fileName']
                status, reason = swift.file_delete(token, daobase.getTenantOSIDByName(tName),
                    container, file_all)
                if(status == 204):
                    messages.add_message(request, messages.SUCCESS, status, 'SUCCESS')
                    messages.add_message(request, messages.SUCCESS, 'delete successful', 'SUCCESS')
                else:
                    messages.add_message(request, messages.ERROR, status, 'ERROR')
                    messages.add_message(request, messages.ERROR, reason, 'ERROR')
            return redirect('/cloudStorage/display/%s' % (container + '/' + path))
        else:
            messages.add_message(request, messages.ERROR, 'select your project.')
            return redirect('/cloudStorage/project/select/')
    else:
        messages.add_message(request, messages.WARNING, 'Please login first.', 'WARNING')
        return redirect('/login/')

@csrf_exempt
def file_download(request):
    lName = request.session.get('name', False)
    tName = request.session.get('tenant', False)
    token = request.session.get('token', False)
    if lName:
        if tName and token:
            if(request.method == 'POST'):
                container = request.POST['containerName']
                path = request.POST['filePath']
                print request.POST['fileName']
            return redirect('/cloudStorage/display/%s' % (container + '/' + path))
        else:
            messages.add_message(request, messages.ERROR, 'select your project.')
            return redirect('/cloudStorage/project/select/')
    else:
        messages.add_message(request, messages.WARNING, 'Please login first.', 'WARNING')
        return redirect('/login/')

