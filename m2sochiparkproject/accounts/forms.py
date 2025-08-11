from django import forms
from base.utils import get_username_type, prettify_phone_number
from django.contrib.auth import get_user_model
import uuid
from django.core.exceptions import ValidationError
from django_recaptcha.fields import ReCaptchaField
from accounts.models import OTPCode, SessionOTPCode

User = get_user_model()


class OTPSecureAuthForm(forms.Form):
    code = forms.CharField(label="Код", max_length=6)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        super().__init__(*args, **kwargs)

    def clean_code(self):
        code = self.cleaned_data.get("code")
        uid = self.request.session.get("otp_uid")

        try:
            otp = OTPCode.objects.get(uuid=uid)
        except OTPCode.DoesNotExist:
            raise ValidationError("Код не найден. Пожалуйста, попробуйте авторизоваться снова.")

        # if otp.is_verified:
        #     raise ValidationError("Код уже подтвержден.")

        if otp.is_expired():
            raise ValidationError("Срок действия кода истёк.")

        if otp.attempt_count >= 5:
            raise ValidationError("Превышено количество попыток.")

        if otp.code != code:
            otp.increment_attempts()
            raise ValidationError("Неверный код.")
        
        if otp.code == code:
            otp.is_verified = True
        
        otp.save()

        return code
    

class OTPSecureRegForm(forms.Form):
    code = forms.CharField(label="Код", max_length=6)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super().__init__(*args, **kwargs)

    def clean_code(self):
        uid = self.request.session.get("otp_uid")
        try:
            otp = SessionOTPCode.objects.get(uuid=uid)
        except SessionOTPCode.DoesNotExist:
            raise forms.ValidationError("OTP не найден.")

        # if otp.is_verified:
        #     raise forms.ValidationError("Код уже подтверждён.")

        if otp.is_expired():
            raise forms.ValidationError("Код истёк.")

        if otp.attempt_count >= 5:
            raise forms.ValidationError("Превышено количество попыток.")

        input_code = self.cleaned_data['code']
        if otp.code != input_code:
            otp.increment_attempts()
            raise forms.ValidationError("Неверный код.")
        
        if otp.code == input_code:
            otp.is_verified = True
        
        otp.save()

        return input_code

class RegisterForm(forms.Form):
    last_name = forms.CharField(label="Фамилия", required=True)
    first_name = forms.CharField(label="Имя", required=True)
    middle_name = forms.CharField(label="Отчество", required=False)
    email = forms.EmailField(label="Email", required=True) 
    phone = forms.CharField(label="Телефон", required=True)
    company_name = forms.CharField(label="Компания", required=True)
    post = forms.CharField(label="Должность", required=True)
    city = forms.CharField(label="Город")

    def clean_email(self):
        email = self.cleaned_data.get('email').lower().strip()
        user_details = User.objects.filter(email=email)
        if user_details.exists():
            raise forms.ValidationError("Аккаунт уже существует, попробуйте авторизоваться!")
        return email.lower().strip()
    
    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        phone_number = prettify_phone_number(raw_phone=phone)
        user_details = User.objects.filter(phone=phone_number)
        if user_details.exists():
            raise forms.ValidationError("Аккаунт уже существует, попробуйте авторизоваться!")
        return phone_number
    
    def get_user_extra_data(self):
        data = {
            'email': self.cleaned_data.get('email').lower().strip(),
            'phone': self.cleaned_data.get('phone'),
            'first_name': self.cleaned_data.get('first_name').title().strip(),
            'last_name': self.cleaned_data.get('last_name').title().strip(),
        }
        return data
    
    def get_member_profile_data(self):
        data = {
            'post': self.cleaned_data.get('post'),
            'company_name': self.cleaned_data.get('company_name'),
            'middle_name': self.cleaned_data.get('middle_name').title().strip(),
            'city': self.cleaned_data.get('city').title().strip(),
        }
        return data


class LoginForm(forms.Form):
    email = forms.EmailField(label="Email")
    
    def clean_email(self):
        email = self.cleaned_data.get('email').lower().strip()
        user_details = User.objects.filter(email=email)
        if not user_details.exists():
            raise forms.ValidationError("Аккаунт не найден. Попробуйте зарегистрироваться.")
        return email.lower().strip()


class LkCaptchaLogin(forms.Form):
    captcha = ReCaptchaField(label='reCaptcha')


class OTPSecureWizard(forms.Form):
    code = forms.IntegerField(label="Код подтверждения")
    
    def clean_code(self):
        return int(self.cleaned_data.get('code'))
