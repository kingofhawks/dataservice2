# coding=utf-8
# import os
# import sys
# print (os.getcwd() + '/../dataService2/')
from django.shortcuts import render_to_response
from django.shortcuts import redirect
from django.contrib import messages
from django.http import HttpResponse
from django.db import connection
from dao import daozo
from osao import keystone

def index(request):
    name = lName = request.session.get('name', False)
    if lName:
        'test'
    return render_to_response('sc/index.html', locals())
#
#
#
#
#
