# Шаблон TMP
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

# Профиль PRF
PRF_01_PROFILE_REG = {
    'id': 'PRF_01_PROFILE_REG',
    'create_notification': False,
    'title': 'Поздравляем с регистрацией в личном кабинете.',
    'text': 'Вы зарегистрировались в личном кабинете.\n\nСсылка в <a href="[LK_LINK]" target="_blank">личный кабинет</a>.',
    'email_topic': 'Регистрация в личном кабинете',
    'email_path': 'emails/01_BLANK_TEMPLATE.html',
    'send_to_email': True,
    'is_published': False,
}

PRF_02_PROFILE_AUTH_CODE = {
    'id': 'PRF_02_PROFILE_AUTH_CODE',
    'create_notification': False,
    'title': 'Код авторизации в личном кабинете.',
    'text': 'Ваш код авторизации для входа в личный кабинет: [CODE].',
    'email_topic': 'Ваш код для авторизации в личном кабинете.',
    'email_path': 'emails/01_BLANK_TEMPLATE.html',
    'send_to_email': True,
    'is_published': False,
}

PRF_03_PROFILE_BLOCKED = {
    'id': 'PRF_03_PROFILE_BLOCKED',
    'create_notification': False,
    'title': 'Что-то не так! Ваша учетная запись заблокирована.',
    'text': f'Ваша учетная запись заблокирована. Возможно к ней пытались получить доступ злоумышленники! Чтобы восстановить доступ, свяжитесь с нами через почту <a href="[CONTACT_EMAIL]" target="_blank">[CONTACT_EMAIL]</a>.',
    'email_topic': 'Что-то не так! Ваша учетная запись заблокирована.',
    'email_path': 'emails/01_BLANK_TEMPLATE.html',
    'send_to_email': True,
    'is_published': False,
}
