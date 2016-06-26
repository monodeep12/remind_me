from django.core.exceptions import ValidationError
from django.test import TestCase
from model_mommy import mommy

from .models import Reminders
from .tasks import send_reminder

import arrow
import datetime

# Import Mock if we're running on Python 2
import six

if six.PY3:
    from unittest.mock import patch
else:
    from mock import patch
        

class RemindersTest(TestCase):

    def test_str(self):
        # Arrange
        t = datetime.datetime.now() + datetime.timedelta(minutes = 10)
        reminder = mommy.make(Reminders, id="2662c2d9f3414589b63d7cee423dd37d", 
        email="mono@amagi.com", 
        phone_number="+919945055794",
        date=datetime.datetime.now().date(),
        time=t.time(),
        message="Test message")

        # Assert
        self.assertEqual(str(reminder), "2662c2d9f3414589b63d7cee423dd37d")

    # def test_clean_invalid_time(self):
    #     # Arrange
    #     t = datetime.datetime.now() - datetime.timedelta(minutes = 10)
    #     reminder = mommy.make(Reminders, 
    #     email="mono@amagi.com", 
    #     phone_number="+919945055794",
    #     date=datetime.datetime.now().date(),
    #     time=t.time(),
    #     message="Test message")

    #     # Assert
    #     with self.assertRaises(ValidationError):
    #         reminder.clean()

    def test_clean_valid_reminder(self):
        # Arrange
        t = datetime.datetime.now() + datetime.timedelta(minutes = 10)
        reminder = mommy.make(Reminders, 
        email="mono@amagi.com", 
        phone_number="+919945055794",
        date=datetime.datetime.now().date(),
        time=t.time(),
        message="Test message")
        
        # Assert
        try:
            reminder.clean()
        except ValidationError:
            self.fail('reminder with time in the past raised ValidationError')

    def test_schedule_reminder(self):
        # Arrange
        t = datetime.datetime.now() + datetime.timedelta(minutes = 10)
        reminder = mommy.make(Reminders, 
        email="mono@amagi.com", 
        phone_number="+919945055794",
        date=datetime.datetime.now().date(),
        time=t.time(),
        message="Test message")

        # Act
        with patch.object(send_reminder, 'apply_async') as mock:
            reminder.schedule_reminder()

        # Assert
        self.assertTrue(mock.called)

    def test_save_initial_creation(self):
        # Act
        with patch.object(Reminders, 'schedule_reminder', return_value=123) as mock:
            t = datetime.datetime.now() + datetime.timedelta(minutes = 10)
            reminder = mommy.make(Reminders, 
            email="mono@amagi.com", 
            phone_number="+919945055794",
            date=datetime.datetime.now().date(),
            time=t.time(),
            message="Test message")

        # Assert
        self.assertTrue(mock.called)
        self.assertEqual(reminder.task_id, 123)