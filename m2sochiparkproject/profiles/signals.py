from django.dispatch import Signal
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from profiles.models import Profile, ProfileHistory
from django.contrib.auth import get_user_model

User = get_user_model()

@receiver(post_save, sender=Profile, dispatch_uid='creata_profile_history_signal')
def creata_profile_history(sender, instance=None, created=False, **kwargs):
    if created:
        ProfileHistory.objects.create(
            user=instance.user,
            company_name=instance.company_name,
            post=instance.post,
            first_name=instance.user.first_name,
            last_name=instance.user.last_name,
            phone=instance.user.phone,
            email=instance.user.email,
            middle_name=instance.middle_name,
            city=instance.city,
        )

@receiver(pre_save, sender=Profile)
def save_profile_history(sender, instance, **kwargs):
    if not instance.pk:
        return  # новая запись — нет изменений

    try:
        old_instance = Profile.objects.get(pk=instance.pk)
    except Profile.DoesNotExist:
        return

    if (
        old_instance.company_name != instance.company_name or
        old_instance.post != instance.post or
        old_instance.city != instance.city
    ):
        ProfileHistory.objects.create(
            user=instance.user,
            company_name=old_instance.company_name,
            post=old_instance.post,
            first_name=old_instance.user.first_name,
            last_name=old_instance.user.last_name,
            phone=old_instance.user.phone,
            email=old_instance.user.email,
            city=old_instance.city,
            middle_name=old_instance.middle_name,
        )


@receiver(pre_save, sender=User)
def save_profile_history_user(sender, instance, **kwargs):
    if not instance.pk:
        return  # новая запись — нет изменений

    try:
        old_instance = User.objects.get(pk=instance.pk)
    except Profile.DoesNotExist:
        return

    if (
        old_instance.first_name != instance.first_name or 
        old_instance.last_name != instance.last_name or
        old_instance.phone != instance.phone or
        old_instance.email != instance.email
    ):
        ProfileHistory.objects.create(
            user=instance,
            first_name=old_instance.first_name,
            last_name=old_instance.last_name,
            phone=old_instance.phone,
            email=old_instance.email,
            company_name=old_instance.user_profile.company_name,
            post=old_instance.user_profile.post,
            city=old_instance.user_profile.city,
            middle_name=old_instance.user_profile.middle_name,
        )
