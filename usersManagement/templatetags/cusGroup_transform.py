'''
Created on 2013-4-10

@author: YUWANG
'''
from django import template
from db.models import *
from django.db import connection

register = template.Library()


@register.tag(name="trans_discount")
def trans_discount(parser, token):
    try:
        tokenString = token.split_contents()
    except ValueError:
        msg = '%r tag requires a single argument' % token.split_contents()[0]
        raise template.TemplateSyntaxError(msg)

    return getDiscount(tokenString[1])


class getDiscount(template.Node):
    def __init__(self, tokenString):
        self.tokenString = tokenString

    def render(self, context):
        discountId = template.resolve_variable(self.tokenString, context)

        if discountId:
            discountInfo = discount.objects.filter(id=discountId)
            discountValue = discountInfo[0].discountValue
        else:
            discountValue = "None"
       #cursor=connection.cursor()
       #cursor.execute("""select d.discountValue from groupDiscountService gcs,discount d where gcs.customerGroupId=%s and gcs.discountId=d.id""",[cusGroupId])
       #discountValue = cursor.fetchall()

        return discountValue


@register.tag(name="trans_product")
def trans_product(parser, token):
    try:
        tokenString = token.split_contents()
    except ValueError:
        msg = '%r tag requires a single argument' % token.split_contents()[0]
        raise template.TemplateSyntaxError(msg)

    return getProduct(tokenString[1])


class getProduct(template.Node):
    def __init__(self, tokenString):
        self.tokenString = tokenString

    def render(self, context):
        productIdStr = template.resolve_variable(self.tokenString, context)

       #products = groupDiscountService.objects.filter(customerGroupId=cusGroupId)
        if productIdStr:
           #productIdStr=products[0].productId

            productNameList = []
            products = product.objects.all()
            for productValue in products:
                if str(productValue.id) in productIdStr:
                    productNameList.append(productValue.name)
           #strList=productIdStr.lstrip("[").rstrip("]").split(",")
            productNameStr = "<br/>".join(productNameList)
        else:
            productNameStr = "None"

        return productNameStr

