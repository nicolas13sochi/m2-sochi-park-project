import datetime
from uuid import UUID

from django.core.management.base import BaseCommand

import argparse
from itertools import islice
import time
import sys
from base.management.commands.consts import USER_FIRST_NAMES, USER_LAST_NAMES, USER_MIDDLE_NAMES, PNONE_TEMPLATE, COMPANY_NAMES, COMPANY_ROLES, CITIES
import random
from django.contrib.auth import get_user_model
from base.management.commands.helpers import create_fake_email

User = get_user_model()

class Command(BaseCommand):
    help = '''Create User models'''

    def add_arguments(self, parser):
        parser.add_argument("-e", "--email",dest="email_host", help="Create users with email name (default: @example.com)", default='@example.com')
        parser.add_argument("--delete", dest="delete_flag", help="Delete User rates", action=argparse.BooleanOptionalAction, default=False)
        parser.add_argument("-q", "--quantity", dest="quantity", type=int, help="User quantity (default: 10) min: 1, max: 999", default=10)
        

    def handle(self, *args, **options):
        begin = time.time()

        email_host = options['email_host']
        delete_flag = options['delete_flag']
        quantity = options['quantity']

        user_last_id = User.objects.last().id

        for i in range(quantity):
            print('Prepare data:')
            print(i + 1)
            user_last_id +=1
            gender = ['MALE', 'FEMALE'][random.randint(0,1)]
            first_name = random.choice(USER_FIRST_NAMES.get(gender.lower()))
            last_name = random.choice(USER_LAST_NAMES.get(gender.lower()))
            role = User.Role.MEMBER
            email = f'test{str(user_last_id).zfill(2)}{email_host}'.lower()

            user_profile = {
                'first_name': first_name,
                'last_name': last_name,
                'email': email,
                'role': role,
                'telegram': None,
            }
            print(user_profile)
            new_user = User.objects.create(**user_profile)
            phone = f'{PNONE_TEMPLATE + new_user.id}'
            new_user.phone = phone
            fake_email = create_fake_email(new_user.get_full_name(), new_user.id, email_host)
            new_user.username = fake_email
            new_user.email = fake_email
            new_user.save()
            telegram_random_param = random.choice([None, new_user.phone, new_user.get_full_name()])
            profile_telegram = create_fake_telegram(telegram_random_param)
            member = new_user.user_profile
            member.telegram = profile_telegram
            member.post = random.choice(COMPANY_ROLES)
            member.company_name = random.choice(COMPANY_NAMES)
            member.save()
            user_last_id = new_user.id
        
        finish = time.time()
        self.stdout.write(
                self.style.SUCCESS(f"Создано пользователей: {quantity}. Продолжительность: {finish - begin} секунд. Домен почты: {email_host}. Статус удаления пользователей: {delete_flag}")
            )
