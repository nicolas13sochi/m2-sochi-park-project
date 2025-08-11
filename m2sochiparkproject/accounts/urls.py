from django.urls import path
from accounts import views


urlpatterns = [
    # wizard url
    path('login/', views.UserAuthWizard.as_view(views.UserAuthWizard.FORMS), name='login'),
    path('register/', views.UserRegistrationWizard.as_view(views.UserRegistrationWizard.FORMS), name='register'),
    # url
    path('register/success', views.register_success, name='register_success'),
    path('logout/', views.logout, name='logout'),
]

htmxpatterns = [
    path('login/resend-auth-code', views.resend_otp_auth_code, name='resend_otp_auth_code'),
    path('login/resend-reg-code', views.resend_otp_reg_code, name='resend_otp_reg_code'),
]

urlpatterns += htmxpatterns
