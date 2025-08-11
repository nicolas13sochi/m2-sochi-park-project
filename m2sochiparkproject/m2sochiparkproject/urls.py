"""m2sochiparkproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path, include
from django.conf import settings
from django.conf.urls.static import static
from wagtail.admin import urls as wagtailadmin_urls
from wagtail.documents import urls as wagtaildocs_urls
from wagtail import urls as wagtail_urls

from django.conf.urls import (
    handler400,
    handler403,
    handler404,
    handler500
)

from pages.views import (
    error_400,
    error_403,
    error_404,
    error_500,
    RobotsTxtView
)

secure_admin = f'{settings.ADMIN_PROTECTED_URL}/' if settings.ADMIN_PROTECTED_URL else ''

urlpatterns = [
    # django
    # path(f'{secure_admin}admin/', admin.site.urls),
    # wagtail
    path(f'{secure_admin}cms/', include(wagtailadmin_urls)),
    # documents
    path('documents/', include(wagtaildocs_urls)),
    # wagtail urls
    path('', include(wagtail_urls)),
    # SEO
    path('robots.txt', RobotsTxtView.as_view(content_type='text/plain'), name='robots'),
    # app
    # path('accounts/', include('accounts.urls')),
    path('', include('pages.urls')),
    # path('', include('profiles.urls')),
    # path('services/', include('services.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler400 = error_400
handler403 = error_403
handler404 = error_404
handler500 = error_500
