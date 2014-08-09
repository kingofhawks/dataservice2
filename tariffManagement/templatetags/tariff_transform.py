'''
Created on 2013-3-28

@author: YUWANG
'''
from django import template
from db.models import product


register = template.Library()


@register.tag(name="transform_productDetail")
def transform_productDetail(parser, token):
    try:
        packageStr = token.split_contents()
    except ValueError:
        msg = '%r tag requires a single argument' % token.split_contents()[0]
        raise template.TemplateSyntaxError(msg)

    return getProductName(packageStr[1])


class getProductName(template.Node):
    def __init__(self, packageStr):
        self.packageStr = packageStr

    def render(self, context):
        packageDetail = template.resolve_variable(self.packageStr, context)
        productNameList = []
        products = product.objects.all()
        for productValue in products:
            if str(productValue.id) in packageDetail:
                productNameList.append(productValue.name)

        productNameStr = "<br/>".join(productNameList)

        return productNameStr
