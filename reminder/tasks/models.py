from __future__ import unicode_literals

from django.utils.encoding import python_2_unicode_compatible
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from timezone_field import TimeZoneField
from django.core.validators import RegexValidator
from pyisemail import is_email
import re
import uuid
import arrow
import datetime


@python_2_unicode_compatible
class Reminders(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(null=True)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+919945055726'. Up to 15 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], blank=True, max_length=15, null=True)
    date = models.DateField(null=False)
    time = models.TimeField(null=False)
    message = models.CharField(max_length=250, blank=False, null=False)
    time_zone = TimeZoneField(default='Asia/Kolkata')

    # Additional fields (not for ui)
    task_id = models.CharField(max_length=50, blank=True, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.id
    
    def clean(self):
        """Checks that reminders are not set in the past"""
        if (self.email == '' and self.phone_number == ''):
            raise ValidationError('Email and phone both cannot be empty')
        
        if not self.email == '':
            if not is_email(self.email, check_dns=True):
                raise ValidationError('Invalid email')
       
        if not self.phone_number == '':
            if not self.validate_mobile():
                raise ValidationError('Invalid phone number')
        
        if self.date == '':
            raise ValidationError('Date cannot be empty')
            
        if self.time == '':
            raise ValidationError('Time cannot be empty')
            
        if len(str(self.time).split(":")) == 1:
            raise ValidationError('Time should be of the format "HH:MM:SS"')
            
        if self.message == "":
            raise ValidationError('Message cannot be empty')
        
        reminder_time = arrow.get(datetime.datetime.combine(self.date, self.time), self.time_zone.zone)

        if reminder_time < arrow.utcnow():
            raise ValidationError('You cannot schedule a reminder for the past. Please check your time and time_zone')
                    
    def schedule_reminder(self):
        """Schedules a Celery task to send a reminder """

        # Calculate the correct time to send this reminder
        reminder_time = arrow.get(datetime.datetime.combine(self.date, self.time), self.time_zone.zone)
        reminder_time = reminder_time.replace(seconds=-settings.REMINDER_TIME)
        # Schedule the Celery task
        from .tasks import send_reminder
        result = send_reminder.apply_async((self.id,), eta=reminder_time)

        return result.id
        
    def save(self, *args, **kwargs):
        self.clean()
        super(Reminders, self).save(*args, **kwargs)
        
        # Schedule a new reminder task for this appointment
        self.task_id = self.schedule_reminder()
        
        # Save our reminder again, with the new task_id
        super(Reminders, self).save(*args, **kwargs)
        
    def validate_mobile(self):
        rule = re.compile(r'^\+?1?\d{9,15}$')
        if rule.search(self.phone_number):
            return True
        else:
            return False
