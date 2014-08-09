# Create your views here.

from django.http import *
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_exempt
from utils.common import *
from db.api.sysAdmin import *


''' adminGroup'''


@csrf_exempt
def adminGroupsIndex(request):
    adminGroups = list_admin("adminGroup")
    return render_to_response('sysAdminManagement/adminGroupsIndex.html', locals())


@csrf_exempt
def addAdminGroup(request):
    #adminGroupId = get_id("adminGroup")
    insert_admin(None, request, "adminGroup")
    return HttpResponseRedirect(reverse('sysAdminManagement.views.adminGroupsIndex'))


def editAdminGroupForm(request, pk):
    #adminGroupId = get_currentId(request)
    adminGroupInfo = get_adminInfo(pk, "adminGroup")
    return render_to_response('sysAdminManagement/editAdminGroupform.html', locals())


@csrf_exempt
def editAdminGroup(request):
    edit_adminInfo(request, "adminGroup")
    return HttpResponseRedirect(reverse('sysAdminManagement.views.adminGroupsIndex'))


@csrf_exempt
def delAdminGroup(request, pk):
    #adminGroupId = get_currentId(request)
    delete_admin(pk, "adminGroup")
    return HttpResponseRedirect(reverse('sysAdminManagement.views.adminGroupsIndex'))

'''sysadmin '''


@csrf_exempt
def sysAdminIndex(request):
    sysAdmins = list_admin("sysAdmin")
    adminGroups = list_admin("adminGroup")
    return render_to_response('sysAdminManagement/sysAdminsIndex.html', locals())


@csrf_exempt
def addSysAdmin(request):
    #sysAdminId = get_id("sysAdmin")
    insert_admin(None, request, "sysAdmin")
    return HttpResponseRedirect(reverse('sysAdminManagement.views.sysAdminIndex'))


def editSysAdminForm(request, pk):
    #sysAdminId = get_currentId(request)
    sysAdminInfo = get_adminInfo(pk, "sysAdmin")
    adminGroups = list_admin("adminGroup")
    return render_to_response('sysAdminManagement/editSysAdminform.html', locals())


@csrf_exempt
def editSysAdmin(request):
    edit_adminInfo(request, "sysAdmin")
    return HttpResponseRedirect(reverse('sysAdminManagement.views.sysAdminIndex'))


@csrf_exempt
def delSysAdmin(request, pk):
    #sysAdminId = get_currentId(request)
    delete_admin(pk, "sysAdmin")
    return HttpResponseRedirect(reverse('sysAdminManagement.views.sysAdminIndex'))