'''
Created on 2013-3-25

@author: YUWANG
'''
from django import template

register = template.Library()


@register.filter("truncate_discountId")
def truncate_discountId(idStr, size):
    idSubStr = idStr[size:]
    return idSubStr


@register.filter("truncate_packageId")
def truncate_packageId(idStr, size):
    idSubStr = idStr[size:]
    return idSubStr
