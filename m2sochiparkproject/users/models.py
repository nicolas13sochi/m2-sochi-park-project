from django.db import models
from base.models import BaseModel
from django.db.models import Q
from django.conf import settings
from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin
from django.core.validators import MaxValueValidator, MinValueValidator
import uuid
from django.utils.translation import gettext_lazy as _
from datetime import datetime, timedelta, timezone
from django.apps import apps

# Create your models here.
class CustomUserManager(BaseUserManager):
    def create_superuser(self, email, password, role=None, **other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)
        other_fields.setdefault('role', 'ADMIN')
      
        if other_fields.get('is_staff') is not True:
            raise ValueError('Superuser must be assigned to is_staff=True')
       
        if other_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must be assigned to is_superuser=True')
        user =  self.create_user(email, password, **other_fields)
        user.set_password(password)
        user.save()
        return user

    def create_user(self, email, password=None, **other_fields):
        if not email:
            raise ValueError('Email address is required!')
        email = self.normalize_email(email)
        if password is not None:
            other_fields.setdefault('is_staff', True)
            other_fields.setdefault('is_superuser', False)
            other_fields.setdefault('role', 'STAFF')

            user = self.model(email=email, password=password, **other_fields)
            user.save()
        else:
            other_fields.setdefault('is_superuser', False)
            other_fields.setdefault('is_staff', False)
            other_fields.setdefault('role', 'MEMBER')

            user = self.model(email=email, password=password, **other_fields)
            user.set_unusable_password()
            user.save()

        return user
    

class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = 'ADMIN', _('Администратор')
        STAFF = 'STAFF', _('Сотрудник')
        MEMBER = 'MEMBER', _('Участник')
    
    username = models.EmailField(default='') # Реплика поля email

    email = models.EmailField(_('email'), unique=True)
    
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    role = models.CharField(max_length=50, choices=Role.choices)

    phone = models.CharField(max_length=30, verbose_name='phone', unique=True, blank=True, null=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def get_user_data(self):
        return {
            'first_name': self.first_name,
            'last_name': self.last_name,
            'middle_name': self.user_profile.middle_name,
            'email': self.email,
            'phone': self.phone,
            'company_name': self.user_profile.company_name,
            'post': self.user_profile.post,
            'city': self.user_profile.city
        }
    
    def update_data(self, data):
        self.first_name = data.get('first_name', self.first_name)
        self.last_name = data.get('last_name', self.last_name)
        self.save()

    def save(self, *args, **kwargs):
        # Всегда нижний регистр для email
        self.email = self.email.lower()
        self.username = self.email.lower()
        self.first_name = self.first_name.title().strip()
        self.last_name = self.last_name.title().strip()
        super(User, self).save(*args, **kwargs)
