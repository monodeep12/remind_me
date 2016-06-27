from tastypie.resources import ModelResource
from .models import Reminders
from tastypie.authorization import Authorization
from tastypie.validation import Validation
from pyisemail import is_email
import re


class RemindersResource(ModelResource):
    class Meta:
        queryset = Reminders.objects.all()
        resource_name = 'reminder'
        allowed_methods = ['post']
        authorization = Authorization()
        always_return_data = True
        

def validate_mobile(value):
    rule = re.compile(r'^\+?1?\d{9,15}$')
    if rule.search(value):
        return True
    else:
        return False
