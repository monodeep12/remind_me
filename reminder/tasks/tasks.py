from __future__ import absolute_import

from celery import shared_task
from django.conf import settings

import arrow
import datetime
from .models import Reminders


@shared_task
def send_reminder(reminder_id):
    # Get our reminder from the database
    try:
        reminder = Reminders.objects.get(id=reminder_id)
    except Reminders.DoesNotExist:
        # The Reminder we were trying to remind someone about
        # has been deleted, so we don't need to do anything
        return
        
    body = 'Hi, You have a reminder : {0}.'.format(
        reminder.message
    )
    
    if not reminder.email == "":
        print("Email:", body)
    
    if not reminder.phone_number == "":
        print("SMS:", body)
