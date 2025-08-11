from django.utils import timezone
import uuid
import random
from base.signal_list import prf_02_profile_auth_code_signal
from accounts.models import OTPCode, SessionOTPCode
from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()

def generate_code():
    return str(random.randint(100000, 999999))

def create_or_refresh_session_otp(session_key, email, resend=False):
    otp, created = SessionOTPCode.objects.get_or_create(
        session_key=session_key,
        email=email,
        is_verified=False,
    )

    if not created and not otp.is_expired():
        return otp
    
    if resend:
        if not otp.can_resend():
            return otp  # не обновляем если еще не истек

    otp.code = generate_code()
    otp.created_at = timezone.now()
    otp.modified_at = timezone.now()
    otp.attempt_count = 0
    if resend:
        otp.resend_count += 1
    otp.resend_available_at = timezone.now() + timezone.timedelta(minutes=settings.TOKEN_VALIDITY['RESEND'])
    otp.save()

    # отправка
    print(email, otp.code)
    prf_02_profile_auth_code_signal.send(sender='prf_02_profile_auth_code_signal', user_id=None, email=email, code=otp.code)
    return otp


def create_or_refresh_otp(user, resend=False):
    otp_entry, created = OTPCode.objects.get_or_create(user=user, is_verified=False)

    
    if not created and not otp_entry.is_expired() and not resend:
        return otp_entry  # не обновляем если еще не истек
    
    if resend:
        if not otp_entry.can_resend():
            return otp_entry  # не обновляем если еще не истек

    # иначе обновляем код и время
    otp_entry.code = generate_code()
    otp_entry.created_at = timezone.now()
    otp_entry.modified_at = timezone.now()
    otp_entry.attempt_count = 0
    if resend:
        otp_entry.resend_count += 1
    otp_entry.resend_available_at = timezone.now() + timezone.timedelta(minutes=settings.TOKEN_VALIDITY['RESEND'])
    otp_entry.save()

    # отправка по email
    print(user, otp_entry.code)
    user_id = user.id
    prf_02_profile_auth_code_signal.send(sender='prf_02_profile_auth_code_signal', user_id=user_id, code=otp_entry.code)
    return otp_entry
