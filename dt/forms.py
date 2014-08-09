# encoding: utf-8
from django import forms

class UploadFileForm(forms.Form):    
    #shift to django-crispy-forms
    CATEGORY_CHOICES = (
        ('科学与统计', '科学与统计'),
        ('零售业与服务业', '零售业与服务业'),
        ('地理位置', '地理位置'),
        ('产品', '产品'),
    )
    
    title = forms.CharField(
        widget=forms.TextInput(attrs={'required': "required"}),
        label = "数据名称",
        max_length = 64,
        required = True,  
    )
    description = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 5}),
        label = "描述",
        max_length = 1024,
        required = False,
    )
    category = forms.ChoiceField(
        label = "类别",
        choices=CATEGORY_CHOICES,
    )
    price = forms.FloatField(
        widget=forms.TextInput(attrs={'required': "required",'data-type':"number"}),
        label = "价格",
        required = True,        
    )
#     data_source = forms.ChoiceField(label="请选择数据来源",
#                             widget=forms.RadioSelect(),choices=PAYMENT_CHOICES)
    file  = forms.FileField(
        widget=forms.FileInput(attrs={'required': "required"}),
        label = "请选择数据文件",
        required = True,
    )
    
class DataTradeForm(forms.Form):
    PAYMENT_CHOICES = (
        ('1', "网银支付"),
        ('2', "支付宝: "),
    )
    # although I've abbreviated the model, 'rad' does not appear in the model;
    # it merely provides input to the un-provided clean function
    payment = forms.ChoiceField(label="请选择支付方式",
                            widget=forms.RadioSelect(),choices=PAYMENT_CHOICES)
    