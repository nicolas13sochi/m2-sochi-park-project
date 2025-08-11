from django import forms
from profiles.models import Profile
from base.utils import get_username_type, prettify_phone_number
import datetime
from django.contrib.auth import get_user_model

User = get_user_model()

class ProfileForm(forms.Form):
    first_name = forms.CharField(label="Имя", disabled=True)
    last_name = forms.CharField(label="Фамилия", disabled=True)
    middle_name = forms.CharField(label="Отчество", disabled=True)
    post = forms.CharField(label="Должность", disabled=True)
    company_name = forms.CharField(label="Компания", disabled=True)
    city = forms.CharField(label="Город", disabled=True)
    email = forms.EmailField(label='Email', disabled=True, )
    phone = forms.CharField(label='Телефон', disabled=True)

class UpdateProfileForm(forms.Form):
    last_name = forms.CharField(label="Фамилия")
    first_name = forms.CharField(label="Имя")
    middle_name = forms.CharField(label="Отчество", required=False)
    company_name = forms.CharField(label="Компания")
    post = forms.CharField(label="Должность")
    city = forms.CharField(label="Город")

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name').title().strip()
        if first_name is None:
            raise forms.ValidationError("Поле Имя не может быть пустым")
        return first_name.title().strip()
    
    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name').title().strip()
        if last_name is None:
            raise forms.ValidationError("Поле Фамилия не может быть пустым")
        return last_name.title().strip()
    
    def clean_middle_name(self):
        middle_name = self.cleaned_data.get('middle_name', '').title().strip()
        return middle_name.title().strip()
    
    def clean_post(self):
        post = self.cleaned_data.get('post').strip()
        if post is None:
            raise forms.ValidationError("Поле Должность не может быть пустым")
        return post.strip()
    
    def clean_company_name(self):
        company_name = self.cleaned_data.get('company_name').strip()
        if company_name is None:
            raise forms.ValidationError("Поле Компания не может быть пустым")
        return company_name.strip()
    
    def clean_city(self):
        city = self.cleaned_data.get('city')
        if city is None:
            raise forms.ValidationError("Поле Город не может быть пустым")
        return city
    
    def get_user_extra_data(self):
        data = {
            'first_name': self.cleaned_data.get('first_name').title().strip(),
            'last_name': self.cleaned_data.get('last_name').title().strip(),
        }
        return data
    
    def get_member_profile_data(self):
        data = {
            'post': self.cleaned_data.get('post'),
            'company_name': self.cleaned_data.get('company_name'),
            'city': self.cleaned_data.get('city', ''),
            'middle_name': self.cleaned_data.get('middle_name', '')
        }
        return data
