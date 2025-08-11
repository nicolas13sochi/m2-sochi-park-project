from django.contrib import admin
from accounts.models import OTPCode, SessionOTPCode

# Register your models here.
@admin.register(OTPCode)
class OTPCodeAdmin(admin.ModelAdmin):
    readonly_fields = ('uuid', 'created_at', 'modified_at', 'resend_available_at')

@admin.register(SessionOTPCode)
class SessionOTPCodeAdmin(admin.ModelAdmin):
    readonly_fields = ('uuid', 'created_at', 'modified_at', 'resend_available_at')
