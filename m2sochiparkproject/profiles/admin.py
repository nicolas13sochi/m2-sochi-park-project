from django.contrib import admin
from typing import Any
from profiles.models import Profile, ProfileHistory
from django.db.models.query import QuerySet
from django.http import HttpRequest
from django.utils.html import format_html
from django.conf import settings
from django.shortcuts import render, redirect
from django.urls import path
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

User = get_user_model()


# Register your models here.
@admin.register(ProfileHistory)
class ProfileHistoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    pass
