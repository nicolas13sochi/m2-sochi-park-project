from django.urls import path
from profiles import views


urlpatterns = [
    path('profile', views.get_profile, name='get_profile'),
    path('profile/edit', views.edit_profile, name='edit_profile'),
]

htmxpatterns = [

]

urlpatterns += htmxpatterns
