# coding=utf-8
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Data(models.Model):
    title = models.CharField(verbose_name="名称",max_length=64) 
    description = models.CharField(verbose_name="描述",max_length=1024)
    creator = models.CharField(verbose_name="发布者",max_length=256)   
    createdDate = models.DateField(verbose_name="发布时间")  
    price = models.FloatField(verbose_name="价格",default=0.0)
    category = models.CharField(verbose_name="类别",max_length=128) 
    
'''
test only
'''    
# class Note(models.Model):
#     user = models.ForeignKey(User)
#     pub_date = models.DateTimeField()
#     title = models.CharField(max_length=200)
#     body = models.TextField()
# 
#     def __unicode__(self):
#         return self.title
