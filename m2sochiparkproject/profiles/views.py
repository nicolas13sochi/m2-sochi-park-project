from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from profiles.forms import UpdateProfileForm, ProfileForm
from django.core.paginator import Paginator
from django.template.loader import get_template
from django.contrib import messages
from base.utils import ObjectIdPaginator, get_bool_param
from django.db.models import Q
from datetime import datetime as dt, timezone, timedelta
import datetime
from django.contrib.auth import get_user_model
from base.navigation import get_navigation
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import user_passes_test
from django.http import QueryDict

User = get_user_model()


# Create your views here.
@login_required
def get_profile(request):
    context = {}
    context['page_navigation'] = get_navigation(navbar='profile', sidebar='profile')
    return render(request, 'profiles/profile.html', context=context)

@login_required
@require_http_methods(['GET', 'POST'])
def edit_profile(request):
    context = {}
    form = UpdateProfileForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            user = request.user
            user_data = form.get_user_extra_data()
            user.update_data(data=user_data)
            profile = user.user_profile
            member_profile_data = form.get_member_profile_data()
            profile.update_data(data=member_profile_data)
            return redirect('get_profile')
    context['form'] = form
    context['page_navigation'] = get_navigation(navbar='profile', sidebar='profile')
    return render(request, 'profiles/profile-edit.html', context=context)
