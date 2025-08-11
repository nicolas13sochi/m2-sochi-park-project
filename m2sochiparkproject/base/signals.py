from django.dispatch import Signal
from django.dispatch import receiver
from django.conf import settings
from base.tasks import send_user_notification
from base.signal_list import (
    # PRF
    prf_01_profile_reg_signal,
    prf_02_profile_auth_code_signal,
    prf_03_profile_blocked_signal,
)
from base.scenarios import PRF_01_PROFILE_REG, PRF_02_PROFILE_AUTH_CODE, PRF_03_PROFILE_BLOCKED

# PRF
"""
Отправка уведомлений PRF
"""
@receiver(prf_01_profile_reg_signal, dispatch_uid='prf_01_profile_reg_signal')
def prf_01_profile_reg(sender, user_id, **kwargs):
    print('Signal:', sender)
    kwargs.pop('signal', None)
    if settings.ASYNC_NOTIFICATION_SEND:
        send_user_notification.delay(user_id=user_id, scenario=PRF_01_PROFILE_REG, **kwargs)
    else:
        send_user_notification(user_id=user_id, scenario=PRF_01_PROFILE_REG, **kwargs)


@receiver(prf_02_profile_auth_code_signal, dispatch_uid='prf_02_profile_auth_code_signal')
def prf_02_profile_auth_code(sender, user_id, **kwargs):
    """
    Для процесса регистрации user=None, но kwargs должен сожержать email
    """
    print('Signal:', sender)
    kwargs.pop('signal', None)
    if settings.ASYNC_NOTIFICATION_SEND:
        send_user_notification.delay(
            user_id=user_id,
            scenario=PRF_02_PROFILE_AUTH_CODE,
            **kwargs
            )
    else:
        send_user_notification(
            user_id=user_id,
            scenario=PRF_02_PROFILE_AUTH_CODE,
            **kwargs
            )


@receiver(prf_03_profile_blocked_signal, dispatch_uid='prf_03_profile_blocked_signal')
def prf_03_profile_blocked(sender, user_id, **kwargs):
    print('Signal:', sender)
    kwargs.pop('signal', None)
    if settings.ASYNC_NOTIFICATION_SEND:
        send_user_notification.delay(user_id=user_id, scenario=PRF_03_PROFILE_BLOCKED,  **kwargs)
    else:
        send_user_notification(user_id=user_id, scenario=PRF_03_PROFILE_BLOCKED,  **kwargs)