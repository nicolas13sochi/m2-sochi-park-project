from __future__ import absolute_import, unicode_literals
from celery import shared_task
import datetime as dt
from datetime import datetime, timedelta, timezone
from base.utils import send_msg_to_group_tg
from typing import Any
from base.utils import send_notification_django
from django.contrib.auth import get_user_model

User = get_user_model()

@shared_task(name='print_message')
def print_message(message, *args, **kwargs):
    print(f'Celery is working!! Message is {message}')


@shared_task(name='print_time')
def print_time():
    now = datetime.now()
    current_time = now.strftime('%H:%M:%S')
    print(f'Current Time is {current_time}')
  

@shared_task(name='print_calculate')
def print_calculate(val1, val2):
    total = val1 + val2
    return total

@shared_task(name='staff_notification_tg')
def send_tg_group_notification(text):
    send_status = send_msg_to_group_tg(text=text)
    return send_status

@shared_task(name='send_user_notification')
def send_user_notification(user_id, scenario, **kwargs):
    print(kwargs)
    send_status = send_notification_django(
        user_id=user_id,
        scenario=scenario,
        **kwargs
    )
