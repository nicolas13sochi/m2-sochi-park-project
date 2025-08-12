from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.views.generic import TemplateView
from pages.forms import LeadForm
from django.views.decorators.http import require_http_methods
from base.handlers import post_lead
from django.contrib import messages

# Create your views here.
def index(request):
    context = {}
    return render(request, 'pages/index.html')

def confidential(request):
    context = {}
    return render(request, 'pages/confidential.html', context=context)


def personal_data(request):
    context = {}
    return render(request, 'pages/personal-data.html', context=context)


def oferta(request):
    context = {}
    return render(request, 'pages/oferta.html', context=context)


def cookies(request):
    context = {}
    return render(request, 'pages/cookies.html', context=context)

class RobotsTxtView(TemplateView):
    template_name = "robots.txt"

@require_http_methods(['POST'])
def create_lead(request):
    form = LeadForm(request.POST or None)
    if form.is_valid():
        data = form.get_lead_data()
        # Add request META to data
        user_agent = request.META.get('HTTP_USER_AGENT', '')
        request_from = request.META.get('HTTP_REFERER', 'Не указан')
        data['user_agent'] = user_agent
        data['request_from'] = request_from
        # Request to lead service
        # TODO: Temporary before M2 Leads Project deploy
        try:
            send_status = post_lead(data=data)
        except:
            messages.error(request, 'Произошла ошибка! Попробуйте снова.')
        if send_status == 201:
            messages.success(request, 'Ваша заявка успешно принята! Мы скоро свяжемся с вами.')
        elif send_status == 400:
            messages.warning(request, 'Произошла ошибка! Попробуйте снова.')
        else:
            messages.error(request, 'Произошла ошибка! Попробуйте снова.')
    return redirect('/')

def error_400(request, exception):
    context = {
        'error_code': 400,
        'error_text': 'Некорректный запрос',
        'error_description': 'Возможно, вы перешли по ссылке, в которой была допущена ошибка, или ресурс был удален'
    }
    return render(request, 'errors/error.html', context=context)

def error_403(request, exception):
    context = {
        'error_code': 403,
        'error_text': 'Доступ к ресурсу запрещен',
        'error_description': 'Возможно, вы перешли по ссылке, в которой была допущена ошибка, или ресурс был удален'
    }
    return render(request, 'errors/error.html', context=context)

def error_404(request, exception):
    context = {
        'error_code': 404,
        'error_text': 'К сожалению, запрашиваемая страница не найдена',
        'error_description': 'Возможно, вы перешли по ссылке, в которой была допущена ошибка, или ресурс был удален'
    }
    return render(request, 'errors/error.html', context=context)

def error_500(request):
    context = {
        'error_code': 500,
        'error_text': 'Внутренняя ошибка сервера',
        'error_description': 'Возможно, вы перешли по ссылке, в которой была допущена ошибка, или ресурс был удален'
    }
    return render(request, 'errors/error.html', context=context)