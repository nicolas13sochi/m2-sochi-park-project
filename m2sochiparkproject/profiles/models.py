from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from base.models import BaseModel
from django.conf import settings
import uuid
from django.core.exceptions import ValidationError
import re

User = get_user_model()

# Create your models here.
class Profile(BaseModel):
    class ProfileType(models.TextChoices):
        MAIN = 'MAIN', _('Основной')
        SPUTNIK = 'SPUTNIK', _('Сопровождение взрослый')
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, editable=False, related_name='user_profile')
    profile_type = models.CharField(max_length=50, choices=ProfileType.choices, default=ProfileType.MAIN, verbose_name='Тип профиля')
    middle_name = models.CharField(max_length=150, blank=True, default='', verbose_name='Отчество')
    post = models.CharField(max_length=150, blank=True, default='', verbose_name='Должность')
    company_name = models.CharField(max_length=150, blank=True, default='', verbose_name='Компания')
    city = models.CharField(max_length=150, blank=True, default='', verbose_name='Город')
    # TODO: Механизм подтверждения ключевых полей пользователя
    is_email_approved = models.BooleanField(default=False, verbose_name='Email подтвержден (да/нет)')
    is_phone_approved = models.BooleanField(default=False, verbose_name='Телефон подтвержден (да/нет)')
    related_to_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='related_to_user', verbose_name='Привязка к пользователю', help_text='')
    notice = models.TextField(blank=True, default='', verbose_name='Заметка', help_text='Используется для пометок в карточке профиля')


    def __str__(self):
        return f'Profile: {self.user} ({self.id})'
    
    
    def clean(self):
        super().clean()
        if self.profile_type == Profile.ProfileType.SPUTNIK:
            if self.related_to_user is None:
                raise ValidationError({'related_to_user': 'Профиль SPUTNIK должен быть привязан к основному профилю участника (MAIN)'})
            if not bool(self.post):
                raise ValidationError({'post': 'Профиль SPUTNIK требует наличия поля Должность'})
            if not bool(self.company_name):
                raise ValidationError({'company_name': 'Профиль SPUTNIK требует наличия поля Компания'})
            if not bool(self.sputnik_email):
                raise ValidationError({'sputnik_email': 'Профиль SPUTNIK требует наличия поля Email спутника'})
            if not bool(self.sputnik_phone):
                raise ValidationError({'sputnik_phone': 'Профиль SPUTNIK требует наличия поля Телефон спутника'})
    
    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)

    
    @property
    def first_name(self):
        return f'{self.user.first_name}'
    
    @property
    def last_name(self):
        return f'{self.user.last_name}'
    
    @property
    def email(self):
        return f'{self.user.email}'
    
    def update_data(self, data):
        self.post = data.get('post', self.post)
        self.company_name = data.get('company_name', self.company_name)
        self.city = data.get('city', self.city)
        self.middle_name = data.get('middle_name', self.middle_name)
        self.save()

    def update_extra_profile(self, data):
        if data.get('profile_type') == 'SPUTNIK':
            self.post = data.get('post', self.post)
            self.company_name = data.get('company_name', self.company_name)
            self.middle_name = data.get('middle_name', self.middle_name)
            self.sputnik_email = data.get('sputnik_email', self.sputnik_email)
            self.sputnik_phone = data.get('sputnik_phone', self.sputnik_phone)
            self.related_to_user = data.get('related_to_user', self.related_to_user)
            self.profile_type = self.ProfileType.SPUTNIK
        self.save()
    
    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'


class ProfileHistory(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, editable=False, related_name='user_profile_history')
    post = models.CharField(max_length=150, blank=True, default='', verbose_name='Должность')
    company_name = models.CharField(max_length=150, blank=True, default='', verbose_name='Компания')
    first_name = models.CharField(max_length=150, blank=True, default='', verbose_name='Имя')
    last_name = models.CharField(max_length=150, blank=True, default='', verbose_name='Фамилия')
    middle_name = models.CharField(max_length=150, blank=True, default='', verbose_name='Отчество')
    phone = models.CharField(max_length=150, blank=True, default='', verbose_name='Телефон', null=True)
    city = models.CharField(max_length=150, blank=True, default='', verbose_name='Город')
    email = models.CharField(max_length=150, blank=True, default='', verbose_name='Email')

    class Meta:
        verbose_name = 'История профиля'
        verbose_name_plural = 'Истории профиля'
