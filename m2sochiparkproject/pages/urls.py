from django.urls import path
from pages import views


urlpatterns = [
    # path('', views.index, name='index'),
    # path('confidential', views.confidential, name='confidential'),
    # path('pd', views.personal_data, name='personal_data'),
    # path('oferta', views.oferta, name='oferta'),
    # path('cookies', views.cookies, name='cookies'),
    path('forms/send', views.create_lead, name='create_lead'),
]
