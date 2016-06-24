from tastypie.resources import ModelResource
from .models import Reminders
from tastypie.authorization import Authorization
from tastypie.validation import Validation
from pyisemail import is_email
import re

class ReminderValidation(Validation):
    """
    Validate user input
    """
    def is_valid(self, bundle, request=None):
        if not bundle.data:
            return {'__all__': 'No data provided.'}
        errors = {}
        if (bundle.data.get('email', '') == '' and bundle.data.get('phone_number', '') == ''):
            errors['phone_number'] = 'At least one field is required'
            errors['email'] = 'At least one field is required'
        
        if not bundle.data.get('email', '') == '':
            if not is_email(bundle.data.get('email'), check_dns=True):
                errors['email'] = 'Invalid email id'
                
        if not bundle.data.get('phone_number', '') == '':
            if not validate_mobile(bundle.data.get('phone_number')):
                errors['phone_number'] = 'Invalid phone number'
                
        if bundle.data.get('date', '') == '':
            errors['date'] = 'Date cannot be empty'
            
        if bundle.data.get('time', '') == '':
            errors['time'] = 'Time cannot be empty'
            
        if len(bundle.data.get('time', '').split(":")) == 1:
            errors['time'] = 'Time should be of the format "HH:MM:SS"'
            
        if bundle.data.get('message', '') == '':
            errors['message'] = 'Message cannot be empty'
        return errors


class RemindersResource(ModelResource):
    class Meta:
        queryset = Reminders.objects.all()
        resource_name = 'reminder'
        allowed_methods = ['post']
        authorization = Authorization()
        validation = ReminderValidation()
        always_return_data = True
        


def validate_mobile(value):
    rule = re.compile(r'^\+?1?\d{9,15}$')
    if rule.search(value):
        return True
    else:
        return False