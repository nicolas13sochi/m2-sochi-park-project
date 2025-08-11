import datetime
import random
from functools import wraps
import time
import requests
from django.template.loader import render_to_string
from phonenumber_field.phonenumber import PhoneNumber
from django.conf import settings
from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError
import uuid
from django.core.mail import send_mail
from django.contrib.auth import get_user_model

User = get_user_model()


def timer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"Execution time of {func.__name__}: {end - start} seconds")
        return result
    return wrapper


def generate_hex_year():
    return f'{datetime.date.today().year:x}'


def generate_code_number():
    return random.randint(100000, 999999)

def get_datetime_now_delta_tz(delta=None):
    if delta is not None:
        return datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(seconds=delta)
    return datetime.datetime.now(datetime.timezone.utc)

class ObjectIdPaginator:
    def __init__(self, qs=None, obj_id=None):
        self.qs_ids = None
        self.current_id = None
        self.next_id = None
        self.previous_id = None

        self.set_ids(qs, obj_id)

    def set_ids(self, qs, obj_id):
        self.qs_ids = list(qs.values_list('id', flat=True))
        self.current_id = obj_id
        current_id_index = self.qs_ids.index(self.current_id)
        qs_total = qs.count()
        self.next_id = self.qs_ids[current_id_index + 1] if current_id_index + 1 < qs_total else self.qs_ids[0]
        self.previous_id = self.qs_ids[current_id_index - 1]


def get_bool_param(value):
    """
    convert string to bool
    """
    if value:
        return value.lower() in ("true",)
    else:
        return False

def validate_email(email):
    validator = EmailValidator()
    try:
        validator(email)
        return True
    except ValidationError:
        return False


def get_username_type(data: str):
    username_type = {
        'email': False,
        'phone': False,
    }
    # TODO: написать Regex валидаторы
    # Email
    if validate_email(data):
        username_type['email'] = True
        return username_type['email'], username_type['phone']
    # Phone
    else:
        if data.startswith('8'):
            data = f'+7{data[1:]}'
        data_ = data if data.startswith('+') else f'+{data}'
        try:
            phone_number = PhoneNumber.from_string(data_)
        except Exception as error:
            print(error)
        else:
            username_type['phone'] = phone_number.is_valid()
        return username_type['email'], username_type['phone']
    
def prettify_phone_number(raw_phone):
    if raw_phone.startswith('8'):
        raw_phone = f'+7{raw_phone[1:]}'
    phone = raw_phone if raw_phone.startswith('+') else f'+{raw_phone}'
    try:
        phone_number = PhoneNumber.from_string(phone)
    except Exception as error:
        raise ValidationError("Некорректный номер телефона!")
    else:
        return f'{phone_number.country_code}{phone_number.national_number}'
    

def send_sms_message(phone_number, user_name, code, **kwargs):
    """
    # Функция отправки СМС через СМС Aero
    """
    if settings.SEND_SERVICE_BY_TG:
        text = f'Код авторизации: {code}. Пользователь: {phone_number}'
        send_msg_to_group_tg(text=text)

    if not settings.SEND_SERVICE_SMS:
        print(phone_number, user_name, code)
        return
    if not all([bool(settings.SMS_AERO_EMAIL), bool(settings.SMS_AERO_API_KEY), bool(settings.SMS_AERO_SIGN)]):
        return
    
    SMS_AERO_EMAIL = settings.SMS_AERO_EMAIL
    SMS_AERO_API_KEY = settings.SMS_AERO_API_KEY
    number = phone_number
    user_name = user_name
    text = 'Ваш код авторизации в личный кабинет: {0}'.format(code)
    sign = settings.SMS_AERO_SIGN
    channel = 'DIRECT'
    BASE_URL = 'https://{0}:{1}@gate.smsaero.ru/v2/sms/send?number={2}&text={3}&sign={4}&channel={5}'.format(SMS_AERO_EMAIL, SMS_AERO_API_KEY, number, text, sign, channel)
    print(BASE_URL)
    r = requests.get(BASE_URL)
    print(r.json())
    return r.json()


def send_email_with_django_backend(to_email, email_topic=None, text=None, email_path=None, **kwargs):
    """
    subject
    message
    from_email
    recipient_list
    fail_silently
    """
    if text is not None:
        kwargs['text'] = text
        kwargs['email_topic'] = email_topic
    print('kwargs:', kwargs)
    code = kwargs.get('code', None)
    if settings.SEND_SERVICE_BY_TG and code is not None:
        text = f'Код авторизации: {code}. Пользователь: {to_email}'
        send_msg_to_group_tg(text=text)

    if not settings.SEND_SERVICE_EMAIL:
        print(to_email, email_topic, text, kwargs)
        return
    

    # Подготовка данных
    from_email = settings.EMAIL_HOST_USER
    subject = email_topic
    to_email = to_email
    if email_path:
        message_html = render_to_string(email_path, context=kwargs)
    else:
        message_html = text if text is not None else subject
    
    response = send_mail(
        subject=subject,
        message=text,
        from_email=from_email,
        recipient_list=[to_email],
        fail_silently=False,
        html_message=message_html,
    )
    return bool(response)

def is_valid_uuid(value):
    try:
        uuid.UUID(str(value))
        return True
    except ValueError:
        return False


def send_msg_to_group_tg(text, chat_id=settings.TG_GROUP_CHAT_ID):
    """
    Send message to telegram group / channel by telegram bot
    """
    if settings.TG_BOT_TOKEN is None:
        print('Не указаны настройки Telegram для группы')
        return False
    params = {
        'text': text,
        'chat_id': chat_id,
        'parse_mode': 'HTML',
    }
    send_url = f'https://api.telegram.org/bot{settings.TG_BOT_TOKEN}/sendMessage'
    response = requests.post(send_url, params=params)
    print(response.json())
    if response.status_code == 200:
        return True
    return False

def send_notification_django(user_id, scenario, **kwargs):
    """
    [СИНХРОННАЯ ВЕРСИЯ]
    Создание и отправка Уведомления согласно сценариев
    TMP_01_TEMPLATE_BLANK = {
        'id': 'TMP_01_TEMPLATE_BLANK',
        'create_notification': False,
        'title': '',
        'text': '',
        'email_topic': '',
        'email_path': '',
        'send_to_email': False,
        'is_published': False,
    }
    TODO: Можно создать модель Notification для хранения логов и отображения уведомлений
    """
    if user_id is None:
        user = None
        email = kwargs.get('email')
    else:
        # Пользователь
        user = User.objects.get(id=user_id)
        email = user.email
    
    create_notification = scenario.get('create_notification', False)
    title = scenario.get('title', '')
    text = scenario.get('text', '')
    email_topic = scenario.get('email_topic', '')
    email_path = scenario.get('email_path', '')
    send_to_email = scenario.get('send_to_email', False)
    is_published = scenario.get('is_published', True)

    # Преобразование текста из **kwargs
    # PRF_01_PROFILE_REG --> prf_01_profile_reg_signal
    if scenario.get('id', '-') == 'PRF_01_PROFILE_REG':
        # [LK_LINK] --> lk_link
        lk_link = kwargs.get('lk_link', '#')
        text = text.replace('[LK_LINK]', lk_link)
    # PRF_02_PROFILE_AUTH_CODE --> prf_02_profile_auth_code_signal
    elif scenario.get('id', '-') == 'PRF_02_PROFILE_AUTH_CODE':
        # [CODE] --> code
        code = kwargs.get('code', 'XXXXXX')
        text = text.replace('[CODE]', code)
    # PRF_03_PROFILE_BLOCKED --> prf_03_profile_blocked_signal
    elif scenario.get('id', '-') == 'PRF_03_PROFILE_BLOCKED':
        # TODO: DO NOT USE YET
        # [CONTACT_EMAIL] --> contact_email
        contact_email = kwargs.get('contact_email', '#')
        text = text.replace('[CONTACT_EMAIL]', contact_email)
    
    # Отправка email
    if send_to_email:
        # Параметры email
        to_email = email
        # Процесс отправки
        email_send_status = send_email_with_django_backend(
            to_email=to_email,
            email_topic=email_topic,
            text=text,
            email_path=email_path,
            **kwargs
        )
