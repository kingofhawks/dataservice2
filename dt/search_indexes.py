import datetime
from haystack import indexes
from models import Data

#Test only  
# class NoteIndex(indexes.SearchIndex, indexes.Indexable):
#     text = indexes.CharField(document=True, use_template=True)
#     author = indexes.CharField(model_attr='user')
#     pub_date = indexes.DateTimeField(model_attr='pub_date')
# 
#     def get_model(self):
#         return Note
# 
#     def index_queryset(self, using=None):
#         """Used when the entire index for model is updated."""
#         #result = self.get_model().objects.filter(pub_date__lte=datetime.datetime.now())
#         result = self.get_model().objects.all()
#         print str(result)+"****NoteIndex**********"
#         return result
    
  
class DataIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    creator = indexes.CharField(model_attr='creator')
    createdDate = indexes.DateTimeField(model_attr='createdDate')
 
    def get_model(self):
        return Data
     
    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        #result = self.get_model().objects.filter(pub_date__lte=datetime.datetime.now())
        result = self.get_model().objects.all()
        print str(result)+"****DataIndex**********"
        return result
