from django.conf.urls import url, include
from tastypie.api import Api
from .api import RemindersResource

v1_api = Api(api_name='v1')
v1_api.register(RemindersResource())

urlpatterns = [url(r'^api/', include(v1_api.urls))]