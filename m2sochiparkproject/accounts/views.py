from django.shortcuts import render, redirect, HttpResponse, HttpResponseRedirect, get_object_or_404
from django.urls import reverse
from django.views.decorators.http import require_http_methods
from django.contrib import auth
from django.contrib import messages
from accounts.forms import (
    LoginForm, 
    RegisterForm, 
    OTPSecureAuthForm,
    OTPSecureRegForm,
    )
from accounts.models import SessionOTPCode, OTPCode
from accounts.utils import create_or_refresh_session_otp, create_or_refresh_otp
from base.utils import get_username_type, prettify_phone_number
from django.contrib.auth import get_user_model
from django.forms.models import model_to_dict
from datetime import datetime, timedelta
from base.tasks import send_tg_group_notification
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from formtools.wizard.views import SessionWizardView
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.http import JsonResponse
from django.utils import timezone
from base.signal_list import prf_01_profile_reg_signal


User = get_user_model()

# Create your views here.
class UserAuthWizard(SessionWizardView):
    FORMS = [
        ('login_input', LoginForm),
        ('code_auth', OTPSecureAuthForm),
    ]

    TEMPLATES = {
        'login_input': 'accounts/login.html',
        'code_auth': 'accounts/auth-code.html',
    }

    #file_storage = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'temp_uploads'))

    def get_template_names(self):
        return [self.TEMPLATES[self.steps.current]]

    def process_step(self, form):
        data = self.get_all_cleaned_data()
        return super().process_step(form)
    
    def render_next_step(self, form, **kwargs):
        if self.steps.current == 'login_input':
            data = self.get_cleaned_data_for_step('login_input')
            # TODO: Fake user behaviour
            user = User.objects.get(email=data.get('email'))  # или session-based

            otp_entry = create_or_refresh_otp(user)
            self.request.session['otp_uid'] = str(otp_entry.uuid)

        return super().render_next_step(form, **kwargs)
    
    def get_form_kwargs(self, step=None):
        kwargs = super().get_form_kwargs(step)
        if step == 'code_auth':
            kwargs.update({'request': self.request})
        return kwargs

    def done(self, form_list, **kwargs):
        data = self.get_all_cleaned_data()
        uid = self.request.session.get('otp_uid')
        otp = OTPCode.objects.get(uuid=uid, is_verified=True)
        user = otp.user
        auth.login(self.request, user, backend='users.auth_backend.PasswordlessAuthBackend')
        # TODO: Удалять или обновлять otp
        otp.delete()
        return HttpResponseRedirect(reverse('index'))

    def get_context_data(self, form, **kwargs):
        context = super().get_context_data(form=form, **kwargs)
        context.update({
            'current_step_name': self.steps.current,
            'total_steps': len(self.FORMS),
            'current_step_number': [x[0] for x in list(self.FORMS)].index(self.steps.current) + 1,
            'progress_percentage': (
                ([x[0] for x in list(self.FORMS)].index(self.steps.current) + 1) * 100 / len(self.FORMS),
            ),
            'email': f"{self.get_cleaned_data_for_step('login_input').get('email')}" if self.steps.current == 'code_auth' else '',
            'otp': OTPCode.objects.get(uuid=self.request.session.get('otp_uid')) if self.steps.current == 'code_auth' else ''
        })
        return context


@login_required
def register_success(request):
    context = {}
    return render(request, 'accounts/register-success.html', context=context)


class UserRegistrationWizard(SessionWizardView):
    FORMS = [
        ('basic_info', RegisterForm),
        ('code', OTPSecureRegForm),
    ]

    TEMPLATES = {
        'basic_info': 'accounts/register.html',
        'code': 'accounts/register-code.html',
    }

    #file_storage = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'temp_uploads'))

    def get_template_names(self):
        return [self.TEMPLATES[self.steps.current]]

    def process_step(self, form):
        data = self.get_all_cleaned_data()
        return super().process_step(form)
    
    def render_next_step(self, form, **kwargs):
        if self.steps.current == 'basic_info':
            data = self.get_cleaned_data_for_step('basic_info')
            email = data.get('email')

            if not self.request.session.session_key:
                self.request.session.create()

            otp = create_or_refresh_session_otp(self.request.session.session_key, email)
            self.request.session['otp_uid'] = str(otp.uuid)

        return super().render_next_step(form, **kwargs)
    
    def get_form_kwargs(self, step=None):
        kwargs = super().get_form_kwargs(step)
        if step == 'code':
            kwargs.update({'request': self.request})
        return kwargs

    def done(self, form_list, **kwargs):
        data = self.get_all_cleaned_data()
        uid = self.request.session.get('otp_uid')
        otp = SessionOTPCode.objects.get(uuid=uid, is_verified=True)
        email = otp.email
        # Create User
        user_data = {
            'email': data['email'].lower().strip(),
            'phone': data['phone'],
            'first_name': data['first_name'].title().strip(),
            'last_name': data['last_name'].title().strip(),
        }
        user = User.objects.create_user(**user_data, password=None)

        profile_data = {
            'post': data['post'],
            'company_name': data['company_name'],
            'middle_name': data['middle_name'],
            'city': data['city'],
        }
        # Update Profile
        profile = user.user_profile
        profile.update_data(data=profile_data)

        auth.login(self.request, user, backend='users.auth_backend.PasswordlessAuthBackend')
        # TODO: Удалять или обновлять otp
        otp.delete()
        # TG
        text = f'Зарегистрирован новый пользователь:\n\nФИО: {user.first_name} {user.last_name}\nКомпания: {user.user_profile.company_name}\nДолжность: {user.user_profile.post}\n\n#модерация'
        send_tg_group_notification(text)
        # PRF_01_PROFILE_REG
        if profile.profile_type == 'MAIN':
            user_id = user.id
            prf_01_profile_reg_signal.send(sender='prf_01_profile_reg_signal', user_id=user_id, lk_link=f'{settings.BASE_URL}/profile')
        #self.file_storage.delete_temporary_files()
        
        return HttpResponseRedirect(reverse('register_success'))

    def get_context_data(self, form, **kwargs):
        context = super().get_context_data(form=form, **kwargs)
        context.update({
            'current_step_name': self.steps.current,
            'total_steps': len(self.FORMS),
            'current_step_number': [x[0] for x in list(self.FORMS)].index(self.steps.current) + 1,
            'progress_percentage': (
                ([x[0] for x in list(self.FORMS)].index(self.steps.current) + 1) * 100 / len(self.FORMS),
            ),
            'email': f"{self.get_cleaned_data_for_step('basic_info').get('email')}" if self.steps.current == 'code' else ''
        })
        return context

@login_required
def logout(request):
    auth.logout(request)
    return redirect('login')

@require_http_methods(['POST'])
def resend_otp_auth_code(request):
    context = {}
    uid = request.session.get('otp_uid')
    otp_entry = OTPCode.objects.get(uuid=uid, is_verified=False)
    user = otp_entry.user
    otp = create_or_refresh_otp(user, resend=True)
    context['otp'] = otp
    return render(request, template_name='accounts/partials/_resend-auth-code.html', context=context)

@require_http_methods(['POST'])
def resend_otp_reg_code(request):
    context = {}
    uid = request.session.get('otp_uid')
    otp = SessionOTPCode.objects.get(uuid=uid, is_verified=False)
    email = otp.email
    session_key = otp.session_key
    otp = create_or_refresh_session_otp(session_key=session_key, email=email, resend=True)
    context['otp'] = otp
    return render(request, template_name='accounts/partials/_resend-reg-code.html', context=context)
