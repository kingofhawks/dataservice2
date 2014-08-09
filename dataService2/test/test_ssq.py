# coding=utf-8
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template.loader import get_template
from django.template import Context
from django.contrib import messages
from django.db import connection
from django.template import RequestContext
from dao import dao_ssq
import datetime
import time

def ssq(request):
    all_list = dao_ssq.get_all()
    # my = [06, 07, 14, 21, 22, 24, 13] #1
    # my = [06, 07, 14, 21, 22, 24, 3] #2
    # my = [06, 07, 14, 21, 22, 0, 13] #3
    # my = [06, 07, 14, 21, 22, 0, 0]  # 4-1
    # my = [06, 07, 14, 21, 0, 0, 13]  # 4-2
    # my = [06, 07, 14, 21, 0, 0, 0]  # 5-1
    # my = [06, 07, 14, 0, 0, 0, 13]  # 5-2
    # my = [06, 07, 14, 0, 0, 0, 13] #6
    my = [2, 8, 11, 16, 25, 31, 9]
    zhong_list = []
    n_r = []
    zhong_count = 0
    zhong_all = 0
    for i in range (0, len(all_list)):
        rec = all_list[i][2].split(' ')
        rec_int = []
        for j in range(0, 7):
            rec_int.append(int(rec[j]))
        # print rec_int
        blue = same_bule(my, rec_int)
        red = same_red(my , rec_int)
        if(blue == 0):
            if(red == 4):
                zhong_count = zhong_count + 1
                n_r = []
                n_r.append(str(all_list[i][0]))
                for b in range(1, len(all_list[i])-1):
                    n_r.append(all_list[i][b])
                n_r.append(str(wu()))
                zhong_list.append(n_r)
                zhong_all = zhong_all + wu()
            elif(red == 5):
                zhong_count = zhong_count + 1
                n_r = []
                n_r.append(str(all_list[i][0]))
                for b in range(1, len(all_list[i])-1):
                    n_r.append(all_list[i][b])
                n_r.append(str(si()))
                zhong_list.append(n_r)
                zhong_all = zhong_all + si()
            elif(red == 6):
                zhong_count = zhong_count + 1
                n_r = []
                n_r.append(str(all_list[i][0]))
                for b in range(1, len(all_list[i])-1):
                    n_r.append(all_list[i][b])
                n_r.append(str(er()))
                zhong_list.append(n_r)
                zhong_all = zhong_all + er()
            else:
                ling()
        elif(blue == 1):
            if(red < 3):
                zhong_count = zhong_count + 1
                n_r = []
                n_r.append(str(all_list[i][0]))
                for b in range(1, len(all_list[i])-1):
                    n_r.append(all_list[i][b])
                n_r.append(str(liu()))
                zhong_list.append(n_r)
                zhong_all = zhong_all + liu()
                #print zhong_list
            if(red == 3):
                zhong_count = zhong_count + 1
                n_r = []
                n_r.append(str(all_list[i][0]))
                for b in range(1, len(all_list[i])-1):
                    n_r.append(all_list[i][b])
                n_r.append(str(wu()))
                zhong_list.append(n_r)
                zhong_all = zhong_all + wu()
            elif(red == 4):
                zhong_count = zhong_count + 1
                n_r = []
                n_r.append(str(all_list[i][0]))
                for b in range(1, len(all_list[i])-1):
                    n_r.append(all_list[i][b])
                n_r.append(str(si()))
                zhong_list.append(n_r)
                zhong_all = zhong_all + si()
                si()
            elif(red == 5):
                zhong_count = zhong_count + 1
                n_r = []
                n_r.append(str(all_list[i][0]))
                for b in range(1, len(all_list[i])-1):
                    n_r.append(all_list[i][b])
                n_r.append(str(san()))
                zhong_list.append(n_r)
                zhong_all = zhong_all + san()
            elif(red == 6):
                zhong_count = zhong_count + 1
                n_r = []
                n_r.append(str(all_list[i][0]))
                for b in range(1, len(all_list[i])-1):
                    n_r.append(all_list[i][b])
                n_r.append(str(yi()))
                zhong_list.append(n_r)
                zhong_all = zhong_all + yi()
            else:
                ling()
        else:
            print 'error'
    return render_to_response('hello/ssq.html', locals())

def same_bule(my, rec):
    if(my[6] == rec[6]):
        return 1
    else:
        return 0

def same_red(my, rec):
    count = 0
    for i in range(0, 6):
        for j in range(0, 6):
            if(my[i] == rec[j]):
                count = count + 1
    return count

def yi():
    return 5000000
    # print '1'
def er():
    return 100000
    # print '2'
def san():
    return 3000
    # print '3'
def si():
    return 200
    # print '4'
def wu():
    return 10 
    # print '5'
def liu():
    return 5
    # print '6'
def ling():
    pass
#
#
#
#
#
