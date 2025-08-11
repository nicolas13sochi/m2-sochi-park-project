from typing import Any
from django.contrib import admin
from django.db.models.query import QuerySet
from django.http import HttpRequest
from users.models import User
from django.contrib.auth.admin import UserAdmin


# Register your models here.
class CustomUserAdmin(UserAdmin, admin.ModelAdmin):
    list_display = UserAdmin.list_display + ('id','role', 'phone', 'uuid')
    list_filter = UserAdmin.list_filter + ('role',)
    fieldsets = UserAdmin.fieldsets + ((None, {'fields': ['role', 'phone',]}),)
    add_fieldsets = UserAdmin.add_fieldsets + ((None, {'fields': ['role', 'phone']}),)
    

    def get_inline_instances(self, request, obj=None):
        if obj is None:
            return []  # не добавлять inline, если пользователь еще не сохранён
        return super().get_inline_instances(request, obj)


admin.site.register(User, CustomUserAdmin)
