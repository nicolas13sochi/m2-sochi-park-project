from django.apps import apps
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.core.signals import setting_changed
from django.dispatch import receiver
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from profiles.models import Profile
from django.contrib.auth import get_user_model

User = get_user_model()


@receiver(setting_changed, dispatch_uid='user_model_swapped_signal')
def user_model_swapped(*, setting, **kwargs):
    if setting == 'AUTH_USER_MODEL':
        apps.clear_cache()
        User = get_user_model()


@receiver(post_save, sender=User, dispatch_uid='create_member_profile_signal')
def create_member_profile(sender, instance=None, created=False, **kwargs):
    if created:
        instance.username = instance.email
        Profile.objects.create(
                user=instance,
            )
