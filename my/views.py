# coding=utf-8
# import os
# import sys
# print (os.getcwd() + '/../dataService2/')
from django.shortcuts import render_to_response
from django.shortcuts import redirect
from django.http import HttpResponse
from django.db import connection
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from dao import daozo
import time
import datetime

# v2.2, in use
def index(request):
    lName = request.session.get('name', False)
    if lName:
        master = daozo.getMasterOfAccount(lName)
        res = daozo.getAccountInfo(lName)
        id = res[0][0]
        # lName = res[0][1]
        email = res[0][2]
        balance = res[0][3]
        # master = res[0][4]
        customerID = res[0][5]
        lastLogin = res[0][6].strftime('%Y-%m-%d %H:%M:%S')
        createTime = res[0][6].strftime('%Y-%m-%d %H:%M:%S')
        res = daozo.getTenantList(lName)
        if master:
            accType = '子帐号'
        else:
            accType = '主帐号'
            if customerID == None :
                shiming = '未认证'
                shimingHref = True                
            else:
                shiming = '已认证'
                shimingHref = False
        projectList = []
        res = daozo.getTenantList(lName)
        if master:
            for i in range(len(res)):
                tenant = {
                          'name':res[i][0],
                          'role':res[i][1],
                          'desc':res[i][2],
                          'time':res[i][3],
                          }
                projectList.append(tenant)
        else:
            for i in range(len(res)):
                tenant = {
                          'name':res[i][0],
                          'role':res[i][1],
                          'desc':res[i][2],
                          'time':res[i][3],
                          }
                projectList.append(tenant)
        userList = []
        if master:
            userList = []
        else:
            res = daozo.getUserListOfOwner(lName)
            for i in range(len(res)):
                res_tr = daozo.getUser_TenantRole(res[i]['loginName'])
                t_list = []
                r_list = []
                if res_tr:
                    for j in range(len(res_tr)):
                        t_list.append(res_tr[j]['tenant'])
                        r_list.append(res_tr[j]['role'])
                res[i].setdefault('tenants', t_list)
                res[i].setdefault('roles', r_list)
                # u = {
                     # 'loginName':res[i]['loginName'],
                     # 'tenantName':t_list,
                     # 'roleName':r_list,
                     # 'balance':res[i]['balance'],
                     # 'create_at':res[i]['create_at'],
                     # }
                # userList.append(u)
                res[i].setdefault('act_del', '/my/user/delete/?UN=%s' % (res[i]['loginName']))
                res[i].setdefault('act_man', '/my/user/detail/?UN=%s' % (res[i]['loginName']))
                userList.append(res[i])
                
        return render_to_response('my/index.html', locals(), RequestContext(request))
        '''
        master = daozo.getMasterOfAccount(lName)
        userList = []
        res = daozo.getAccountInfo(lName)
        id = res[0][0]
        # lName = res[0][1]
        email = res[0][2]
        balance = res[0][3]
        # master = res[0][4]
        customerID = res[0][5]
        lastLogin = res[0][6].strftime('%Y-%m-%d %H:%M:%S')
        createTime = res[0][6].strftime('%Y-%m-%d %H:%M:%S')
        res = daozo.getTenantList(lName)
        if master:
            accType = '子帐号'
        else:
            accType = '主帐号'
            if customerID == None :
                shiming = '未认证'
                shimingHref = True                
            else:
                shiming = '已认证'
                shimingHref = False    
            # userList = getSubAccount(lName)
        return render_to_response('my/index.html', locals(), RequestContext(request))
        '''
    else:
        messages.add_message(request, messages.WARNING, 'Please login first.', 'WARNING')
        return redirect('/login/')

# deprecated
# def getSubAccount(loginName):
#    userList = []
#    temp = daozo.getSubAccountList(loginName)
#    for i in range(len(temp)):
#        tenant_role = daozo.getTenantByUser(temp[i]['loginName'])
#        t_list = []
#        r_list = []
#        for j in range(len(tenant_role)):
#            t_list.append(tenant_role[j][0])
#            r_list.append(tenant_role[j][1])
#        u = {
#             'loginName':temp[i]['loginName'],
#             'tenantName':t_list,
#             'roleName':r_list,
#             'balance':temp[i]['balance'],
#             'create_at':temp[i]['create_at'],
#             }
#        userList.append(u)
#    return userList

def real_name_the_authentication(request):
    lName = request.session.get('name', False)
    if lName:
        return render_to_response('my/RNTA.html', locals())
    else:
        messages.add_message(request, messages.WARNING, 'Please login first.', 'WARNING')
        return redirect('/login/')

@csrf_exempt
def rnta_submit(request):
    lName = request.session.get('name', False)
    if lName:
        if request.method == 'POST':
            flag = daozo.customer_add(lName, request.POST['name'], request.POST['idNo'],
                request.POST['email'], request.POST['mobile'],
                request.POST['company'], request.POST['address'])
            if flag:
                messages.add_message(request, messages.SUCCESS,
                    'Real name the authentication successful.', 'SUCCESS')
            else:
                messages.add_message(request, messages.ERROR,
                    'Real name the authentication failed.', 'ERROR')
        return redirect('/my/grzl/')
    else:
        messages.add_message(request, messages.WARNING, 'Please login first.', 'WARNING')
        return redirect('/login/')

def grzl(request):
    lName = request.session.get('name', False)
    if lName:
        mcid = daozo.getMCID(lName)
        if(mcid[0][0] is None):
            master = None
        else:
            master = mcid[0][0]
        if(mcid[0][1] == None):
            shiming = False
        else:
            shiming = True
            res = daozo.getCustomerInfoByID(mcid[0][1])
            email = res[0][0]
            realName = res[0][1]
            identi = res[0][2]
            level = res[0][3]
            mobile = res[0][4]
            address = res[0][5]
            company = res[0][6]
            createTime = res[0][7].strftime('%Y-%m-%d %H:%M:%S')
        return render_to_response('my/grzl.html', locals(), RequestContext(request))
    else:
        messages.add_message(request, messages.WARNING, 'Please login first.', 'WARNING')
        return redirect('/login/')

def fwlb(request):
    lName = request.session.get('name', False)
    if lName:
        return render_to_response('my/fwlb.html', locals())
    else:
        return redirect('/login/')

def zybb(request):
    lName = request.session.get('name', False)
    if lName:
        return render_to_response('my/zybb.html', locals())
    else:
        return redirect('/login/')

def jygl(request):
    lName = request.session.get('name', False)
    if lName:
        return render_to_response('my/jygl.html', locals())
    else:
        return redirect('/login/')

def lscx(request):
    lName = request.session.get('name', False)
    if lName:
        return render_to_response('my/lscx.html', locals())
    else:
        return redirect('/login/')

# v2.2 in use
def tenant_list(request):
    lName = request.session.get('name', False)
    if lName:
        master = daozo.getMasterOfAccount(lName)
        projectList = []
        res = daozo.getTenantList(lName)
        if master:
            for i in range(len(res)):
                tenant = {
                          'name':res[i][0],
                          'role':res[i][1],
                          'time':res[i][2],
                          'desc':res[i][3],
                          # 'act_s':True,
                          'url_s':'/virtualHost/project/select/submit/?s=' + res[i][0],
                          # 'act_m':True,
                          'url_m':'/my/project/detail/?PN=' + res[i][0],
                          }
                projectList.append(tenant)
        else:
            for i in range(len(res)):
                tenant = {
                          'name':res[i][0],
                          'role':res[i][1],
                          'time':res[i][2],
                          'desc':res[i][3],
                          # 'act_s':True,
                          'url_s':'/virtualHost/project/select/submit/?s=' + res[i][0],
                          # 'act_m':True,
                          'url_m':'/my/project/detail/?PN=' + res[i][0],
                          # 'act_d':True,
                          'url_d':'/my/project/delete/?PN=' + res[i][0],
                          }
                projectList.append(tenant)
        return render_to_response('my/tenant/tenant_list.html', locals(), RequestContext(request))
    else:
        messages.add_message(request, messages.WARNING, 'Please login first.', 'WARNING')
        return redirect('/login/')

# v2.2 in use
def tenant_detail(request):
    lName = request.session.get('name', False)
    if lName:
        master = daozo.getMasterOfAccount(lName)
        '''
        if master:
            
            messages.add_message(request, messages.ERROR, 'Premission denied.', 'ERROR')
            return redirect('/my/project/list/')
        else:
            tenant = daozo.getTenantDetail(request.GET['PN'])
            if(tenant):
                user_list = daozo.getTenantUserList(tenant['id'])
                tenant.setdefault('users', user_list)
                return render_to_response('my/tenant/tenant_detail.html', locals())
            else:
                messages.add_message(request, messages.ERROR, 'Invalid project.', 'ERROR')
                return redirect('/my/project/list/')
        '''
        tenant = daozo.getTenantDetail(request.GET['PN'])
        if(tenant):
            user_list = daozo.getTenantUserList(tenant['id'])
            tenant.setdefault('users', user_list)
            return render_to_response('my/tenant/tenant_detail.html', locals())            
        else:
            messages.add_message(request, messages.ERROR, 'Invalid project.', 'ERROR')
            return redirect('/my/project/list/')
    else:
        messages.add_message(request, messages.WARNING, 'Please login first.', 'WARNING')
        return redirect('/login/')

# v2.2, in use
def tenant_create(request):
    lName = request.session.get('name', False)
    if lName:
        return render_to_response('my/tenant/tenant_create.html', locals(), RequestContext(request))
    else:
        messages.add_message(request, messages.WARNING, 'Please login first.', 'WARNING')
        return redirect('/login/')

def tenant_create_name_check(request):
    r = daozo.check_tenant_create_name(request.GET['PN'])
    return HttpResponse(r)

@csrf_exempt
def tenant_create_submit(request):
    lName = request.session.get('name', False)
    if lName:
        if request.method == 'POST':
            flag = daozo.tenant_create2(lName, request.POST['tenantName'], request.POST['tenantDesc'])
            if(flag):
                messages.add_message(request, messages.SUCCESS, 'project create successful.')
                return redirect('/my/index/')
            else:
                messages.add_message(request, messages.ERROR, 'project create failed.')
                return render_to_response('my/tenant/tenant_create.html', locals(), RequestContext(request))
    else:
        messages.add_message(request, messages.WARNING, 'Please login first.', 'WARNING')
        return redirect('/login/')

def tenant_delete(request):
    lName = request.session.get('name', False)
    if lName:
        tenant = request.GET['PN']
        res = daozo.getUserCountOfTenant(tenant)
        if(res > 0):
            messages.add_message(request, messages.ERROR, 'There are still other users in this project', 'ERROR')
        else:
            flag = daozo.tenant_delete(tenant)
            if flag:
                messages.add_message(request, messages.SUCCESS, 'project %s delete successful.' % (tenant), 'SUCCESS')
            else:
                messages.add_message(request, messages.ERROR, 'project %s delete failed.' % (tenant), 'ERROR')
        return redirect('/my/project/list/')
    else:
        messages.add_message(request, messages.WARNING, 'Please login first.', 'WARNING')
        return redirect('/login/')

# deprecated
# def tenant_select(request):
#    lName = request.session.get('name', False)
#    pn = request.GET['PN']
#    if lName and pn:
#        pn = "name:" + pn
#    return HttpResponse(pn)
#    # return render_to_response('my/tenant/tenant_detail.html', locals())

# v2.2 in use
def user_list(request):
    lName = request.session.get('name', False)
    if lName:
        master = daozo.getMasterOfAccount(lName)
        userList = []
        if master:
            messages.add_message(request, messages.ERROR, 'Permission denied to view the user list.', 'ERROR')
            return redirect('/my/user/list/')
        else:
            res = daozo.getUserListOfOwner(lName)
            for i in range(len(res)):
                res_tr = daozo.getUser_TenantRole(res[i]['loginName'])
                t_list = []
                r_list = []
                if res_tr:
                    for j in range(len(res_tr)):
                        t_list.append(res_tr[j]['tenant'])
                        r_list.append(res_tr[j]['role'])
                res[i].setdefault('tenants', t_list)
                res[i].setdefault('roles', r_list)
                # u = {
                     # 'loginName':res[i]['loginName'],
                     # 'tenantName':t_list,
                     # 'roleName':r_list,
                     # 'balance':res[i]['balance'],
                     # 'create_at':res[i]['create_at'],
                     # }
                # userList.append(u)
                res[i].setdefault('act_del', '/my/user/delete/?UN=%s' % (res[i]['loginName']))
                res[i].setdefault('act_man', '/my/user/detail/?UN=%s' % (res[i]['loginName']))
                userList.append(res[i])
        return render_to_response('my/user/user_list.html', locals(), RequestContext(request))
    else:
        messages.add_message(request, messages.WARNING, 'Please login first.', 'WARNING')
        return redirect('/login/')

# v2.2, in use
def user_detail(request):
    lName = request.session.get('name', False)
    if lName:
        master = daozo.getMasterOfAccount(lName)
        userList = []
        if master:
            messages.add_message(request, messages.ERROR, 'Permission denied to view the user detail.', 'ERROR')
            return redirect('/my/user/detail/')
        else:
            user = daozo.getUserDetail(request.GET['UN'])
            if(user):
                if (user['master']):
                    user.setdefault('type', 'zizhanghao')
                else:
                    user.setdefault('type', 'zhuzhanghao')
                res_tr = daozo.getUser_TenantRole(user['loginName'])
                user.setdefault('tenants', res_tr)
                return render_to_response('my/user/user_detail.html', locals())
            else:
                messages.add_message(request, messages.ERROR, 'Invalid project.', 'ERROR')
                return redirect('/my/user/list/')
    else:
        messages.add_message(request, messages.WARNING, 'Please login first.', 'WARNING')
        return redirect('/login/')

def user_create(request):
    lName = request.session.get('name', False)
    if lName:
        master = daozo.getMasterOfAccount(lName)
        if master:
            messages.add_message(request, messages.ERROR, 'permission denied, only project owner.')
            return redirect('/my/')
        else:
            return render_to_response('my/user/user_create.html', locals(), RequestContext(request))
    else:
        messages.add_message(request, messages.WARNING, 'Please login first.', 'WARNING')
        return redirect('/login/')

# v2.2, in use
def user_create_name_check(request):
    r = daozo.check_user_create_name(request.GET['UN'])
    return HttpResponse(r)
    
def user_create_submit(request):
    lName = request.session.get('name', False)
    if lName:
        if request.method == 'POST':
            userName = request.POST['userName']
            userPass = request.POST['userPass']
            userEmail = request.POST['userEmail']
            flag = daozo.sub_account_create(lName, userName, userPass , userEmail)
        return redirect('/my/')
    else:
        messages.add_message(request, messages.WARNING, 'Please login first.', 'WARNING')
        return redirect('/login/')

def user_delete(request):
    lName = request.session.get('name', False)
    if lName:
        user = request.GET['UN']
        res = daozo.getTenantCountOfUser(user)
        if(res > 0):
            messages.add_message(request, messages.ERROR, 'user is still in other project', 'ERROR')
        else:
            flag = daozo.sub_account_delete(user)
            if flag:
                messages.add_message(request, messages.SUCCESS, 'sub user delete successful.')
            else:
                messages.add_message(request, messages.ERROR, 'sub user delete failed.')
        return redirect('/my/user/list/')
    else:
        messages.add_message(request, messages.WARNING, 'Please login first.', 'WARNING')
        return redirect('/login/')

# v2.2, in use
def tenant_edit_user(request):
    lName = request.session.get('name', False)
    if lName:
        master = daozo.getMasterOfAccount(lName)
        if master:
            messages.add_message(request, messages.ERROR, 'permission denied, only project owner.')
            return redirect('/my/')
        else:
            tenant = request.GET['t']
            if tenant:
                userList = []
                res = daozo.getUserListOfOwner(lName)
                sys_role_list = daozo.getSysRoleList()
                for i in range(len(res)):
                    res_tr = daozo.getUser_TenantRole(res[i]['loginName'])
                    t_list = []
                    r_list = []
                    res[i].setdefault('current_tenant', False)
                    res[i].setdefault('current_role', False)
                    if res_tr:
                        for j in range(len(res_tr)):
                            if res_tr[j]['tenant'] == tenant:
                                res[i]['current_tenant'] = True
                                res[i]['current_role'] = res_tr[j]['role']
                            else:
                                t_list.append(res_tr[j]['tenant'])
                                r_list.append(res_tr[j]['role'])
                            # res[i].setdefault('desc', res_tr[j]['desc'])
                    res[i].setdefault('tenants', t_list)
                    res[i].setdefault('roles', r_list)
                    userList.append(res[i])
            else:
                messages.add_message(request, messages.ERROR, 'Invalid project.', 'ERROR')
                return redirect('/my/project/list/')
            return render_to_response('my/tenant/tenant_edit_user.html', locals(), RequestContext(request))
    else:
        messages.add_message(request, messages.WARNING, 'Please login first.', 'WARNING')
        return redirect('/login/')

# v2.2, in use
@csrf_exempt
def tenant_edit_user_submit(request):
    lName = request.session.get('name', False)
    if lName:
        master = daozo.getMasterOfAccount(lName)
        if master:
            messages.add_message(request, messages.ERROR, 'permission denied, only project owner.')
            return redirect('/my/')
        else:
            if request.method == 'POST':
                action = request.POST['action']
                tenant = request.POST['tenantName']
                user = request.POST['userName']
                role = request.POST['roleSelect']
                if action == 'add':
                    if(daozo.tenant_add_user(tenant, user, role)):
                        messages.add_message(request, messages.SUCCESS, 'user add successful.', 'SUCCESS')
                    else:
                        messages.add_message(request, messages.ERROR, 'user add failed.', 'ERROR')
                if action == 'del':
                    if role == 'owner':
                        messages.add_message(request, messages.ERROR, 'can not del role owner.', 'ERROR')
                    else:
                        if(daozo.tenant_del_user(tenant, user, role)):
                            messages.add_message(request, messages.SUCCESS, 'user del successful.', 'SUCCESS')
                        else:
                            messages.add_message(request, messages.ERROR, 'user del failed.', 'ERROR')
            return redirect('/my/project/user/edit/?t=%s' % tenant)
    else:
        messages.add_message(request, messages.WARNING, 'Please login first.', 'WARNING')
        return redirect('/login/')

# deprecated
# if __name__ == '__main__':
#    print os.getcwd()
#    print (os.getcwd() + '/../dataService2/')
#    sys.path.append(os.getcwd() + '/../')
#    print sys.path
#
#
#
#
#
