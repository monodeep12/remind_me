from __future__ import unicode_literals

from django.utils.encoding import python_2_unicode_compatible
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from timezone_field import TimeZoneField
from django.core.validators import RegexValidator
import uuid
import arrow


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
        
    def save(self, *args, **kwargs):
        super(Reminders, self).save(*args, **kwargs)