from tastypie.resources import ModelResource
from .models import Reminders
from tastypie.authorization import Authorization
from tastypie.validation import Validation
from pyisemail import is_email
import re
import datetime

class RemindersValidation(Validation):
    def is_valid(self, bundle, request=None):
        if not bundle.data:
            return {'__all__': 'No data provided.'}
        errors = {}
        
        email = bundle.data.get('email', '')
        phone_number = bundle.data.get('phone_number', '')
        date = bundle.data.get('date', '')
        time = bundle.data.get('time', '')
        message = bundle.data.get('message', '')
        time_zone = bundle.data.get('time_zone', '')
        
        
        if (email == '' and phone_number == ''):
            errors["email"] = 'Email and phone both cannot be empty'
            errors["phone_number"] = 'Email and phone both cannot be empty'
        
        if not email == '':
            if not is_email(email, check_dns=True):
                errors["email"] = 'Invalid email'
       
        if not phone_number == '':
            if not validate_mobile():
                errors["phone_number"] = 'Invalid phone number'
        
        if date == '':
            errors["date"] = 'Date cannot be empty'
            
        if time == '':
            errors["time"] = 'Time cannot be empty'
            
        if len(str(time).split(":")) == 1:
            errors["time"] = 'Time should be of the format "HH:MM:SS"'
            
        if message == "":
            errors["message"] = 'Message cannot be empty'
        
        d = datetime.datetime.strptime(date, "%d/%m/%Y").date()
        t = datetime.datetime.strptime(time, '%H:%M').time()
        reminder_time = arrow.get(
            datetime.datetime.combine(
                d, t), time_zone)

        if reminder_time < arrow.utcnow():
            errors["time"] = 'You cannot schedule a reminder for the past.'
        return errors
        
        
class RemindersResource(ModelResource):
    class Meta:
        queryset = Reminders.objects.all()
        resource_name = 'reminder'
        allowed_methods = ['post']
        authorization = Authorization()
        validation = RemindersValidation()
        always_return_data = True


def validate_mobile(value):
    rule = re.compile(r'^\+?1?\d{9,15}$')
    if rule.search(value):
        return True
    else:
        return False
