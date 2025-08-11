from transliterate import translit
import random


def create_fake_email(full_name, user_id, email_host):
    return '.'.join(translit(full_name, language_code='ru', reversed=True).split(' ')).lower() + f'.{user_id}{email_host}'

def generate_fake_profile_data():
    res = {
        'user': {},
        'profile': {}
    }
