from django.db import models
from django.utils import timezone
import uuid
from django.conf import settings
from base.models import BaseModel
from django.contrib.auth import get_user_model

User = get_user_model()
# Create your models here.
class OTPModel(BaseModel):
    code = models.CharField(max_length=6)
    attempt_count = models.PositiveIntegerField(default=0)
    resend_count = models.PositiveIntegerField(default=0)
    is_verified = models.BooleanField(default=False)
    resend_available_at = models.DateTimeField(auto_now_add=True, null=True)

    def is_expired(self):
        return timezone.now() - self.created_at > timezone.timedelta(minutes=settings.TOKEN_VALIDITY['CODE'])

    def increment_attempts(self):
        self.attempt_count += 1
        self.save()

    def can_resend(self):
        return timezone.now() >= self.resend_available_at

    def mark_resend(self):
        self.resend_available_at = timezone.now() + timezone.timedelta(minutes=settings.TOKEN_VALIDITY['RESEND'])
        self.resend_count += 1
        self.save()

    def delta_resend(self):
        if self.resend_available_at is None:
            return 0
        elif self.resend_available_at < timezone.now():
            return 0
        else:
            return (self.resend_available_at - timezone.now()).seconds

    def clear_params(self):
        self.attempt_count = 0
        self.resend_count = 0
        self.is_verified = False
        self.resend_available_at = timezone.now()
        self.save()


    class Meta:
        abstract = True

class OTPCode(OTPModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    class Meta:
        verbose_name = 'Код авторизации'
        verbose_name_plural = 'Коды авторизации'

    

class SessionOTPCode(OTPModel):
    session_key = models.CharField(max_length=40)  # из request.session.session_key
    email = models.EmailField()

    class Meta:
        verbose_name = 'Код регистрации'
        verbose_name_plural = 'Коды регистрации'
