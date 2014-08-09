from tastypie.resources import ModelResource
from tastypie.authorization import Authorization
from models import Data
from authentication import ExtendedApiKeyAuthentication


class DataResource(ModelResource):
    class Meta:
        queryset = Data.objects.all()
        resource_name = 'data'
        authorization = Authorization()#No authorization
        authentication = ExtendedApiKeyAuthentication()