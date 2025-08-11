from dotenv import load_dotenv
import os

# ENV PARAMS CONFIG
# TODO: Add .env filepath support from project root directory
load_dotenv()
ENV_SETTINGS = bool(int(os.getenv('ENV_SETTINGS', False)))

if ENV_SETTINGS:
    SECRET_KEY = os.getenv('SECRET_KEY')
    DEBUG = False if int(os.getenv('DEBUG')) == 0 else True
    ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS').split(',') if os.getenv('ALLOWED_HOSTS') else []
    if bool(os.getenv('CSRF_TRUSTED_ORIGINS')):
        CSRF_TRUSTED_ORIGINS = os.getenv('CSRF_TRUSTED_ORIGINS').split(',')

    EMAIL_BACKEND = os.getenv('EMAIL_BACKEND', 'django.core.mail.backends.console.EmailBackend')
    EMAIL_HOST = os.getenv('EMAIL_HOST', 'localhost')
    EMAIL_PORT = os.getenv('EMAIL_PORT', 25)
    EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER', '')
    EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD', '')
    EMAIL_USE_TLS = False if int(os.getenv('EMAIL_USE_TLS')) == 0 else True
    EMAIL_USE_SSL = False if int(os.getenv('EMAIL_USE_SSL')) == 0 else True

    SEND_SERVICE_EMAIL = bool(int(os.getenv('SEND_SERVICE_EMAIL', False)))
    SEND_SERVICE_SMS = bool(int(os.getenv('SEND_SERVICE_SMS', False)))
    SEND_SERVICE_BY_TG = bool(int(os.getenv('SEND_SERVICE_BY_TG', False)))

    TG_BOT_TOKEN = os.getenv('TG_BOT_TOKEN', None)
    TG_BASE_URL = os.getenv('TG_BASE_URL', None)
    TG_GROUP_CHAT_ID = os.getenv('TG_GROUP_CHAT_ID', None)

    # Telegram notification Bot
    ASYNC_NOTIFICATION_SEND = False if int(os.getenv('ASYNC_NOTIFICATION_SEND', 1)) == 0 else True

    # ReCaptcha
    RECAPTCHA_PUBLIC_KEY = os.getenv('RECAPTCHA_PUBLIC_KEY', '')
    RECAPTCHA_PRIVATE_KEY = os.getenv('RECAPTCHA_PRIVATE_KEY', '')

    ADMIN_PROTECTED_URL = os.getenv('ADMIN_PROTECTED_URL', '')

    SMS_AERO_EMAIL = os.getenv('SMS_AERO_EMAIL', '')
    SMS_AERO_API_KEY = os.getenv('SMS_AERO_API_KEY', '')

    # CELERY SETTINGS
    CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL', 'redis://localhost:6379') 
    CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND', 'redis://localhost:6379')  
    CELERY_ACCEPT_CONTENT = os.getenv('CELERY_ACCEPT_CONTENT').split(',') if os.getenv('CELERY_ACCEPT_CONTENT') else ['application/json']
    CELERY_TASK_SERIALIZER = os.getenv('CELERY_TASK_SERIALIZER', 'json')  
    CELERY_RESULT_SERIALIZER = os.getenv('CELERY_RESULT_SERIALIZER', 'json')  
    CELERY_TIMEZONE = os.getenv('CELERY_TIMEZONE', 'Europe/Moscow')

    # BASE URL
    BASE_URL = os.getenv('BASE_URL', 'http://127.0.0.1:8000')

    # Lead service
    LEAD_API_KEY = os.getenv('LEAD_API_KEY', None)
    LEAD_API_URL = os.getenv('LEAD_API_URL', None)

    # POSTGRES
    USE_POSTGRES = False if int(os.getenv('USE_POSTGRES')) == 0 else True

    if USE_POSTGRES:

        POSTGRES_NAME = os.getenv('POSTGRES_NAME')
        POSTGRES_USER = os.getenv('POSTGRES_USER')
        POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
        POSTGRES_HOST = os.getenv('POSTGRES_HOST')
        POSTGRES_PORT = os.getenv('POSTGRES_PORT')


        DATABASES = {
            'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': POSTGRES_NAME, 
            'USER': POSTGRES_USER,
            'PASSWORD': POSTGRES_PASSWORD,
            'HOST': POSTGRES_HOST,
            'PORT': POSTGRES_PORT,
            }
        }
