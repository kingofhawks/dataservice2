# coding=utf-8
from django.shortcuts import render_to_response
from django.shortcuts import redirect
from django.contrib import messages
from django.http import HttpResponse
from django.template import RequestContext
from django.db import connection
from django.views.decorators.csrf import csrf_exempt
from dao import daozo
from dao import base as daobase
from osao import token as tokenApi
from osao import nova
from osao import glance
import datetime
from datetime import date
import time

compute_URL = "http://192.168.0.51:8774/v2/"
image_URL = "http://192.168.0.50:9292/v2/"

def index(request):
    lName = request.session.get('name', False)
    tName = request.session.get('tenant', False)
    token = request.session.get('token', False)
    if lName:
        if tName and token:
            return redirect('summary/')
        else:
            return redirect('project/select/')
    else:
        return render_to_response('vh/index.html', locals())

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
                url_s = '/virtualHost/project/select/submit/?s=' + res[i][0]
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
                url_s = '/virtualHost/project/select/submit/?s=' + res[i][0]
                tenant = {
                          'name':res[i][0],
                          'role':res[i][1],
                          'desc':res[i][2],
                          'time':res[i][3],
                          'url_s':url_s,
                          }
                projectList.append(tenant)
#        projectList = []
#        res = daozo.getTenantList(lName)
#        for i in range(len(res)):
#            url_s = '/virtualHost/project/select/submit/?s=' + res[i][0]
#            tenant = {
#                      'name':res[i][0],
#                      'role':res[i][1],
#                      'desc':res[i][2],
#                      'url_s':url_s,
#                      }
#            projectList.append(tenant)
        return render_to_response('vh/project_select.html', locals(), RequestContext(request))
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
        request.session['tenant_id'] = tenant_id
        currentTenant = tenant_name
        currentToken = token
        messages.add_message(request, messages.INFO, 'peoject changed', 'INFO')
        return redirect('/virtualHost/project/select/')
    else:
        messages.add_message(request, messages.WARNING, 'Please login first.', 'WARNING')
        return redirect('/login/')

# replaced by new fun
# def tenant_select(request):
#    lName = request.session.get('name', False)
#    lPass = request.session.get('pass', False)
#    tName = 'dscpTest2'
#    if lName and lPass:
#        t_token = request.session.get('token', False)
#        if(t_token):
#            current_tenant = tName
#            current_token = t_token
#        else:
#            tenant_id = daobase.getTenantOSIDByName(tName)
#            t_token, mes = token.get_tenant_token(lName, lPass, tenant_id)
#            request.session['tenant'] = tName
#            request.session['token'] = t_token
#            current_tenant = tName
#            current_token = t_token
#        return render_to_response('vh/project_select.html', locals(), RequestContext(request))
#    else:
#        messages.add_message(request, messages.WARNING, 'Please login first.', 'WARNING')
#        return redirect('/login/')
#    return render_to_response('vh/summary/summary.html', locals(), RequestContext(request))

@csrf_exempt
def summary(request):
    lName = request.session.get('name', False)
    tName = request.session.get('tenant', False)
    token = request.session.get('token', False)
    if lName:
        if tName and token:
            if request.method == 'POST':
                t1 = request.POST['sDate1']
                t2 = request.POST['sDate2']
                # print t1
                # year = t1[:t1.find('-')]
                # print year
                # left = t1[len(year) + 1:]
                # print left
                # month = t1[len(year) + 1:][:t1[len(year) + 1:].find('-')]
                # print month
                # date = t1[len(year) + 1:][t1[len(year) + 1:].find('-') + 1:]
                # print date
                start = datetime.datetime(int(t1[:t1.find('-')]),
                                          int(t1[len(t1[:t1.find('-')]) + 1:][:t1[len(t1[:t1.find('-')]) + 1:].find('-')]),
                                          int(t1[len(t1[:t1.find('-')]) + 1:][t1[len(t1[:t1.find('-')]) + 1:].find('-') + 1:]),
                                          0, 0, 0, 0).isoformat()
                end = datetime.datetime(int(t2[:t2.find('-')]),
                                        int(t2[len(t2[:t2.find('-')]) + 1:][:t2[len(t2[:t2.find('-')]) + 1:].find('-')]),
                                        int(t2[len(t2[:t2.find('-')]) + 1:][t2[len(t2[:t2.find('-')]) + 1:].find('-') + 1:]),
                                        23, 59, 59, 999999.99).isoformat()
            else:
                now = datetime.datetime.now()
                start = datetime.datetime(now.year, now.month, 1, 0, 0, 0, 0).isoformat()
                end = now.isoformat()
            projectUsage, serverUsageList = nova.tenant_usage(token, daobase.getTenantOSIDByName(tName), start, end)
            return render_to_response('vh/summary/summary.html', locals(), RequestContext(request))
        else:
            messages.add_message(request, messages.ERROR, 'select your project.')
            return redirect('/virtualHost/project/select/')
    else:
        messages.add_message(request, messages.WARNING, 'Please login first.', 'WARNING')
        return redirect('/login/')

def server_list(request):
    lName = request.session.get('name', False)
    tName = request.session.get('tenant', False)
    token = request.session.get('token', False)
    vhList = []
    if lName:
        if tName and token:
            serverList = nova.server_list(token, daobase.getTenantOSIDByName(tName))
            for s in serverList:
                s.setdefault('flavorInfo', nova.flavor_detail(token,
                            daobase.getTenantOSIDByName(tName), s['flavor']['id']))
            return render_to_response('vh/server/server_list.html', locals(), RequestContext(request))
        else:
            messages.add_message(request, messages.ERROR, 'select your project.')
            return redirect('/virtualHost/project/select/')
    else:
        messages.add_message(request, messages.WARNING, 'Please login first.', 'WARNING')
        return redirect('/login/')

def server_detail(request, id):
    lName = request.session.get('name', False)
    tName = request.session.get('tenant', False)
    token = request.session.get('token', False)
    if lName:
        if tName and token:
            serverDetail = nova.get_server_detail(token, daobase.getTenantOSIDByName(tName), id)
            return render_to_response('vh/server/server_detail.html', locals(), RequestContext(request))
        else:
            messages.add_message(request, messages.ERROR, 'select your project.')
            return redirect('/virtualHost/project/select/')
    else:
        messages.add_message(request, messages.WARNING, 'Please login first.', 'WARNING')
        return redirect('/login/')

def server_creat(request):
    lName = request.session.get('name', False)
    tName = request.session.get('tenant', False)
    token = request.session.get('token', False)
    if lName:
        if tName and token:
            sourceTypeList = [{'key':'Image', 'value':'Image'},
                          {'key':'Snapshot', 'value':'Snapshot'}]
            imageList = glance.get_image_list(token)
            snapshotList = glance.get_server_snapshot_list(token)
            flavorList = nova.get_flavor_list(token, daobase.getTenantOSIDByName(tName))
            keypairList = nova.get_keypair_list(token, daobase.getTenantOSIDByName(tName))
            securityGroupList = nova.get_security_group_list(token, daobase.getTenantOSIDByName(tName))
            return render_to_response('vh/server/server_create.html', locals(), RequestContext(request))
        else:
            messages.add_message(request, messages.ERROR, 'select your project.')
            return redirect('/virtualHost/project/select/')
    else:
        messages.add_message(request, messages.WARNING, 'Please login first.', 'WARNING')
        return redirect('/login/')

@csrf_exempt
def server_creat_submit(request):
    lName = request.session.get('name', False)
    tName = request.session.get('tenant', False)
    token = request.session.get('token', False)
    if lName:
        if tName and token:
            if (request.method == 'POST'):
                serverNmae = request.POST['serverName']
                if (request.POST['sourceType'] == 'Image'):
                    imageURL = 'http://192.168.0.50:9292/v2/images/' + request.POST['sourceImageSelect']
                if (request.POST['sourceType'] == 'Snapshot'):
                    imageURL = 'http://192.168.0.50:9292/v2/images/' + request.POST['sourceSnapshotSelect']
                flavorURL = "http://192.168.0.51:8774/v2/%s/flavor/%s" % (
                    daobase.getTenantOSIDByName(tName), request.POST['sourceFlavorSelect'])
                metadata = {}
                # print imageURL
                # print flavorURL
                code, message = nova.server_create(token, daobase.getTenantOSIDByName(tName),
                        serverNmae, imageURL, flavorURL, metadata)
                securityGropURL = "http://192.168.0.51:8774/v2/%s/os-security-groups/%s" % (
                    daobase.getTenantOSIDByName(tName), request.POST['sourceSecurityGropSelect'])
                # print 'securityGroup'
                # print securityGropURL

                # print 'sourceKeypairSelect'
                # print request.POST['sourceKeypairSelect']
                
                # nova.server_create(token, daobase.getTenantOSIDByName(tName), server_name, imageRef, flavorRef, metadata)
                if(code == 200):
                    messages.add_message(request, messages.SUCCESS, code, 'SUCCESS')
                    messages.add_message(request, messages.SUCCESS, message, 'SUCCESS')
                else:
                    messages.add_message(request, messages.ERROR, code, 'ERROR')
                    messages.add_message(request, messages.ERROR, message, 'ERROR')
                return redirect('/virtualHost/server/list/')
            else:
                return redirect('/virtualHost/server/create/')
        else:
            messages.add_message(request, messages.ERROR, 'select your project.')
            return redirect('/virtualHost/project/select/')
    else:
        messages.add_message(request, messages.WARNING, 'Please login first.', 'WARNING')
        return redirect('/login/')

def server_delete(request, id):
    lName = request.session.get('name', False)
    tName = request.session.get('tenant', False)
    token = request.session.get('token', False)
    if lName:
        if tName and token:
            status, reason = nova.server_delete(token, daobase.getTenantOSIDByName(tName), id)
            if(status == 204):
                messages.add_message(request, messages.SUCCESS, status, 'SUCCESS')
                messages.add_message(request, messages.SUCCESS, 'delete successful', 'SUCCESS')
            else:
                messages.add_message(request, messages.ERROR, status, 'ERROR')
                messages.add_message(request, messages.ERROR, reason, 'ERROR')
            return redirect('/virtualHost/server/list/')
        else:
            messages.add_message(request, messages.ERROR, 'select your project.')
            return redirect('/virtualHost/project/select/')
    else:
        messages.add_message(request, messages.WARNING, 'Please login first.', 'WARNING')
        return redirect('/login/')

def server_create_snapshot(request, id):
    lName = request.session.get('name', False)
    tName = request.session.get('tenant', False)
    token = request.session.get('token', False)
    if lName:
        if tName and token:
            serverId = id
            return render_to_response('vh/server/create_snapshot.html',
                                      locals(), RequestContext(request))
        else:
            messages.add_message(request, messages.ERROR, 'select your project.')
            return redirect('/virtualHost/project/select/')
    else:
        messages.add_message(request, messages.WARNING, 'Please login first.', 'WARNING')
        return redirect('/login/')

@csrf_exempt
def server_create_snapshot_submit(request, id):
    lName = request.session.get('name', False)
    tName = request.session.get('tenant', False)
    token = request.session.get('token', False)
    if lName:
        if tName and token:
            if (request.method == 'POST'):
                s_name = request.POST['snapshotName']
                status, reason = nova.server_create_image(token,
                        daobase.getTenantOSIDByName(tName), id, s_name)
                if(status == 202):
                    messages.add_message(request, messages.SUCCESS, status, 'SUCCESS')
                    messages.add_message(request, messages.SUCCESS, 'create successful', 'SUCCESS')
                else:
                    messages.add_message(request, messages.ERROR, status, 'ERROR')
                    messages.add_message(request, messages.ERROR, reason, 'ERROR')
            return redirect('/virtualHost/snapshot/list/')
        else:
            messages.add_message(request, messages.ERROR, 'select your project.')
            return redirect('/virtualHost/project/select/')
    else:
        messages.add_message(request, messages.WARNING, 'Please login first.', 'WARNING')
        return redirect('/login/')
    
def volume_list(request):
    lName = request.session.get('name', False)
    tName = request.session.get('tenant', False)
    token = request.session.get('token', False)
    if lName:
        if tName and token:
            volumeList = nova.get_volume_list(token, daobase.getTenantOSIDByName(tName))
            return render_to_response('vh/volume/volume_list.html', locals(), RequestContext(request))
        else:
            messages.add_message(request, messages.ERROR, 'select your project.')
            return redirect('/virtualHost/project/select/')
    else:
        messages.add_message(request, messages.WARNING, 'Please login first.', 'WARNING')
        return redirect('/login/')

def volume_detail(request, id):
    lName = request.session.get('name', False)
    tName = request.session.get('tenant', False)
    token = request.session.get('token', False)
    if lName:
        if tName and token:
            volumeDetail = nova.volume_detail(token, daobase.getTenantOSIDByName(tName), id)
            return render_to_response('vh/volume/volume_detail.html', locals(), RequestContext(request))
        else:
            messages.add_message(request, messages.ERROR, 'select your project.')
            return redirect('/virtualHost/project/select/')
    else:
        messages.add_message(request, messages.WARNING, 'Please login first.', 'WARNING')
        return redirect('/login/')

def volume_delete(request, id):
    lName = request.session.get('name', False)
    tName = request.session.get('tenant', False)
    token = request.session.get('token', False)
    if lName:
        if tName and token:
            status, reason = nova.volume_delete(token, daobase.getTenantOSIDByName(tName), id)
            if(status == 202):
                messages.add_message(request, messages.SUCCESS, status, 'SUCCESS')
                messages.add_message(request, messages.SUCCESS, 'allocate successful', 'SUCCESS')
            else:
                messages.add_message(request, messages.ERROR, status, 'ERROR')
                messages.add_message(request, messages.ERROR, reason, 'ERROR')
            return redirect('/virtualHost/volume/list/')
        else:
            messages.add_message(request, messages.ERROR, 'select your project.')
            return redirect('/virtualHost/project/select/')
    else:
        messages.add_message(request, messages.WARNING, 'Please login first.', 'WARNING')
        return redirect('/login/')

def volume_create_snapshot(request, id):
    lName = request.session.get('name', False)
    tName = request.session.get('tenant', False)
    token = request.session.get('token', False)
    if lName:
        if tName and token:
            volumeId = id
            return render_to_response('vh/volume/create_snapshot.html',
                                      locals(), RequestContext(request))
        else:
            messages.add_message(request, messages.ERROR, 'select your project.')
            return redirect('/virtualHost/project/select/')
    else:
        messages.add_message(request, messages.WARNING, 'Please login first.', 'WARNING')
        return redirect('/login/')

@csrf_exempt
def volume_create_snapshot_submit(request, id):
    lName = request.session.get('name', False)
    tName = request.session.get('tenant', False)
    token = request.session.get('token', False)
    if lName:
        if tName and token:
            if (request.method == 'POST'):
                s_name = request.POST['snapshotName']
                s_desc = request.POST['snapshotDesc']
                status, reason = nova.volume_create_snapshot(token,
                        daobase.getTenantOSIDByName(tName), s_name, s_desc, id)
                if(status == 200):
                    messages.add_message(request, messages.SUCCESS, status, 'SUCCESS')
                    messages.add_message(request, messages.SUCCESS, 'create successful', 'SUCCESS')
                else:
                    messages.add_message(request, messages.ERROR, status, 'ERROR')
                    messages.add_message(request, messages.ERROR, reason, 'ERROR')
            return redirect('/virtualHost/snapshot/list/')
        else:
            messages.add_message(request, messages.ERROR, 'select your project.')
            return redirect('/virtualHost/project/select/')
    else:
        messages.add_message(request, messages.WARNING, 'Please login first.', 'WARNING')
        return redirect('/login/')

def volume_delete_snapshot(request, id):
    lName = request.session.get('name', False)
    tName = request.session.get('tenant', False)
    token = request.session.get('token', False)
    if lName:
        if tName and token:
            status, reason = nova.volume_delete_snapshot(token, daobase.getTenantOSIDByName(tName), id)
            if(status == 202):
                messages.add_message(request, messages.SUCCESS, status, 'SUCCESS')
                messages.add_message(request, messages.SUCCESS, 'allocate successful', 'SUCCESS')
            else:
                messages.add_message(request, messages.ERROR, status, 'ERROR')
                messages.add_message(request, messages.ERROR, reason, 'ERROR')
            return redirect('/virtualHost/snapshot/list/')
        else:
            messages.add_message(request, messages.ERROR, 'select your project.')
            return redirect('/virtualHost/project/select/')
    else:
        messages.add_message(request, messages.WARNING, 'Please login first.', 'WARNING')
        return redirect('/login/')

def image_list(request):
    lName = request.session.get('name', False)
    tName = request.session.get('tenant', False)
    token = request.session.get('token', False)
    if lName:
        if tName and token:
            imageList = glance.get_image_list(token)
            return render_to_response('vh/image/image_list.html', locals(), RequestContext(request))
        else:
            messages.add_message(request, messages.ERROR, 'select your project.')
            return redirect('/virtualHost/project/select/')
    else:
        messages.add_message(request, messages.WARNING, 'Please login first.', 'WARNING')
        return redirect('/login/')

def image_detail(request):
    return render_to_response('vh/image/image_detail.html', locals(), RequestContext(request))

def snapshot_list(request):
    lName = request.session.get('name', False)
    tName = request.session.get('tenant', False)
    token = request.session.get('token', False)
    if lName:
        if tName and token:
            serverSnapshotList = glance.get_server_snapshot_list(token)
            volumeSnapshotList = nova.get_volume_snapshot_list(token, daobase.getTenantOSIDByName(tName))
            return render_to_response('vh/snapshot/snapshot_list.html', locals(), RequestContext(request))
        else:
            messages.add_message(request, messages.ERROR, 'select your project.')
            return redirect('/virtualHost/project/select/')
    else:
        messages.add_message(request, messages.WARNING, 'Please login first.', 'WARNING')
        return redirect('/login/')
    
def snapshot_server_delete(request, id):
    lName = request.session.get('name', False)
    tName = request.session.get('tenant', False)
    token = request.session.get('token', False)
    if lName:
        if tName and token:
            status, reason = glance.image_delete(token, id)
            if(status == 204):
                messages.add_message(request, messages.SUCCESS, status, 'SUCCESS')
                messages.add_message(request, messages.SUCCESS, 'delete successful', 'SUCCESS')
            else:
                messages.add_message(request, messages.ERROR, status, 'ERROR')
                messages.add_message(request, messages.ERROR, reason, 'ERROR')
            return redirect('/virtualHost/snapshot/list/')
        else:
            messages.add_message(request, messages.ERROR, 'select your project.')
            return redirect('/virtualHost/project/select/')
    else:
        messages.add_message(request, messages.WARNING, 'Please login first.', 'WARNING')
        return redirect('/login/')

def flavor_list(request):
    lName = request.session.get('name', False)
    tName = request.session.get('tenant', False)
    token = request.session.get('token', False)
    if lName:
        if tName and token:
            flavorList = nova.get_flavor_list(token, daobase.getTenantOSIDByName(tName))
            return render_to_response('vh/flavor/flavor_list.html', locals(), RequestContext(request))
        else:
            messages.add_message(request, messages.ERROR, 'select your project.')
            return redirect('/virtualHost/project/select/')
    else:
        messages.add_message(request, messages.WARNING, 'Please login first.', 'WARNING')
        return redirect('/login/')

def access_list(request):
    lName = request.session.get('name', False)
    tName = request.session.get('tenant', False)
    token = request.session.get('token', False)
    if lName:
        if tName and token:
            floatingIpList = nova.get_floating_ip_list(token, daobase.getTenantOSIDByName(tName))
            return render_to_response('vh/access/floatingIp_list.html', locals(), RequestContext(request))
        else:
            messages.add_message(request, messages.ERROR, 'select your project.')
            return redirect('/virtualHost/project/select/')
    else:
        messages.add_message(request, messages.WARNING, 'Please login first.', 'WARNING')
        return redirect('/login/')

def floating_ip_allocate(request):
    lName = request.session.get('name', False)
    tName = request.session.get('tenant', False)
    token = request.session.get('token', False)
    if lName:
        if tName and token:
            floatingIpPoolList = nova.get_floating_ip_pool(token, daobase.getTenantOSIDByName(tName))
            return render_to_response('vh/access/floatingIp_allocate.html', locals(), RequestContext(request))
        else:
            messages.add_message(request, messages.ERROR, 'select your project.')
            return redirect('/virtualHost/project/select/')
    else:
        messages.add_message(request, messages.WARNING, 'Please login first.', 'WARNING')
        return redirect('/login/')

@csrf_exempt
def floating_ip_allocate_submit(request):
    lName = request.session.get('name', False)
    tName = request.session.get('tenant', False)
    token = request.session.get('token', False)
    if lName:
        if tName and token:
            if (request.method == 'POST'):
                pool = request.POST['sourcePool']
                status, reason = nova.floating_ip_allocate(token, daobase.getTenantOSIDByName(tName), pool)
                if(status == 200):
                    messages.add_message(request, messages.SUCCESS, status, 'SUCCESS')
                    messages.add_message(request, messages.SUCCESS, 'allocate successful', 'SUCCESS')
                else:
                    messages.add_message(request, messages.ERROR, status, 'ERROR')
                    messages.add_message(request, messages.ERROR, reason, 'ERROR')
            return redirect('/virtualHost/access/list/')
        else:
            messages.add_message(request, messages.ERROR, 'select your project.')
            return redirect('/virtualHost/project/select/')
    else:
        messages.add_message(request, messages.WARNING, 'Please login first.', 'WARNING')
        return redirect('/login/')

def floating_ip_deallocate(request, id):
    lName = request.session.get('name', False)
    tName = request.session.get('tenant', False)
    token = request.session.get('token', False)
    if lName:
        if tName and token:
            status, reason = nova.floating_ip_deallocate(token, daobase.getTenantOSIDByName(tName), id)
            if(status == 202):
                messages.add_message(request, messages.SUCCESS, status, 'SUCCESS')
                messages.add_message(request, messages.SUCCESS, 'deallocate successful', 'SUCCESS')
            else:
                messages.add_message(request, messages.ERROR, status, 'ERROR')
                messages.add_message(request, messages.ERROR, reason, 'ERROR')
            return redirect('/virtualHost/access/list/')
        else:
            messages.add_message(request, messages.ERROR, 'select your project.')
            return redirect('/virtualHost/project/select/')
    else:
        messages.add_message(request, messages.WARNING, 'Please login first.', 'WARNING')
        return redirect('/login/')

def floating_ip_associate(request):
    lName = request.session.get('name', False)
    tName = request.session.get('tenant', False)
    token = request.session.get('token', False)
    if lName:
        if tName and token:
            try:
                ip = request.GET['ip']
                ip = int(ip)
            except:
                ip = ''
            try:
                server = request.GET['server']
            except:
                server = ''
            serverList = nova.server_list(token, daobase.getTenantOSIDByName(tName))
            floatingIpList = nova.get_floating_ip_list(token, daobase.getTenantOSIDByName(tName))
            for i in floatingIpList:
                if i['instance_id']:
                    floatingIpList.remove(i)
            return render_to_response('vh/access/floatingIp_associate.html',
                                      locals(), RequestContext(request))
            return redirect('/virtualHost/access/list/')
        else:
            messages.add_message(request, messages.ERROR, 'select your project.')
            return redirect('/virtualHost/project/select/')
    else:
        messages.add_message(request, messages.WARNING, 'Please login first.', 'WARNING')
        return redirect('/login/')

@csrf_exempt
def floating_ip_associate_submit(request):
    lName = request.session.get('name', False)
    tName = request.session.get('tenant', False)
    token = request.session.get('token', False)
    if lName:
        if tName and token:
            if (request.method == 'POST'):
                ip = request.POST['ip']
                server = request.POST['server']
                status, reason = nova.floating_ip_associate(token,
                        daobase.getTenantOSIDByName(tName), ip, server)
                if(status == 202):
                    messages.add_message(request, messages.SUCCESS, status, 'SUCCESS')
                    messages.add_message(request, messages.SUCCESS, 'associate successful', 'SUCCESS')
                else:
                    messages.add_message(request, messages.ERROR, status, 'ERROR')
                    messages.add_message(request, messages.ERROR, reason, 'ERROR')
            return redirect('/virtualHost/access/list/')
        else:
            messages.add_message(request, messages.ERROR, 'select your project.')
            return redirect('/virtualHost/project/select/')
    else:
        messages.add_message(request, messages.WARNING, 'Please login first.', 'WARNING')
        return redirect('/login/')

def floating_ip_unassociate(request):
    lName = request.session.get('name', False)
    tName = request.session.get('tenant', False)
    token = request.session.get('token', False)
    if lName:
        if tName and token:
            try:
                ip = request.GET['ip']
            except:
                ip = False
            try:
                server = request.GET['server']
            except:
                server = False
            if(ip and server):
                status, reason = nova.floating_ip_unassociate(token,
                                daobase.getTenantOSIDByName(tName), ip, server)
                if(status == 202):
                    messages.add_message(request, messages.SUCCESS, status, 'SUCCESS')
                    messages.add_message(request, messages.SUCCESS, 'unassociate successful', 'SUCCESS')
                else:
                    messages.add_message(request, messages.ERROR, status, 'ERROR')
                    messages.add_message(request, messages.ERROR, reason, 'ERROR')
            return redirect('/virtualHost/access/list/')
        else:
            messages.add_message(request, messages.ERROR, 'select your project.')
            return redirect('/virtualHost/project/select/')
    else:
        messages.add_message(request, messages.WARNING, 'Please login first.', 'WARNING')
        return redirect('/login/')

def keypair_list(request):
    lName = request.session.get('name', False)
    tName = request.session.get('tenant', False)
    token = request.session.get('token', False)
    if lName:
        if tName and token:
            keypairList = nova.get_keypair_list(token, daobase.getTenantOSIDByName(tName))
            return render_to_response('vh/keypair/keypair_list.html', locals(), RequestContext(request))
        else:
            messages.add_message(request, messages.ERROR, 'select your project.')
            return redirect('/virtualHost/project/select/')
    else:
        messages.add_message(request, messages.WARNING, 'Please login first.', 'WARNING')
        return redirect('/login/')

def security_list(request):
    lName = request.session.get('name', False)
    tName = request.session.get('tenant', False)
    token = request.session.get('token', False)
    if lName:
        if tName and token:
            securityGroupList = nova.get_security_group_list(token, daobase.getTenantOSIDByName(tName))
            return render_to_response('vh/security/security_list.html', locals(), RequestContext(request))
        else:
            messages.add_message(request, messages.ERROR, 'select your project.')
            return redirect('/virtualHost/project/select/')
    else:
        messages.add_message(request, messages.WARNING, 'Please login first.', 'WARNING')
        return redirect('/login/')
    
