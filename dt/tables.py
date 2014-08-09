# tutorial/tables.py
import django_tables2 as tables
from dt.models import Data
from django.utils.safestring import mark_safe
from django.utils.html import escape
from django_tables2.utils import A

class ImageColumn(tables.Column):
     def render(self, value):
         return mark_safe('<img src="/media/img/%s.jpg" />'
                         % escape(value))

class DataTable(tables.Table):
    #selection = tables.CheckBoxColumn(accessor="pk", orderable=False)  
    #Customization for Image     
    #name = ImageColumn()
    title = tables.LinkColumn('data_detail', args=[A('pk')])
    class Meta:
        model = Data
        
        #selection = tables.CheckBoxColumn(accessor="pk", orderable=False)
        # add class="paleblue" to <table> tag
        attrs = {"class": "paleblue",'width':'130%'}
        