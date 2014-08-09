from tastypie.authentication import Authentication
from tastypie.authentication import ApiKeyAuthentication
from django.db import connection

#Test only
class SillyAuthentication(Authentication):
    def is_authenticated(self, request, **kwargs):
        if 'daniel' in request.user.username:
          return True
        print 'authentication failed:%s',(request.user.username)
        return False

    # Optional but recommended
    def get_identifier(self, request):
        return request.user.username
    
#http://localhost:8000/market/api/v1/data/?format=json&username=simon&api_key=99dcbc2e0d459a1734f581597e378a5eb9d79d46    
class ExtendedApiKeyAuthentication(ApiKeyAuthentication):
    def is_authenticated(self, request, **kwargs):
        try:
            username, api_key = self.extract_credentials(request)
        except ValueError:
            return self._unauthorized()
        print username,api_key

        cursor = connection.cursor()
        cursor.execute("SELECT id FROM t_account WHERE loginName = %s and apikey = %s", [username,api_key])
        row = cursor.fetchone()
        print row
        if row is not None:
          return True
        print '%s authentication failed:%s',(username,api_key)
        return False