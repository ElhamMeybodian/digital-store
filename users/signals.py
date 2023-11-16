from django.db.models.signals import post_save
from django.dispatch import receiver

from users.models import Profile, User, Device


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if not created and instance.is_active is True:
        try:
            Profile.objects.get_object_or_404(user=instance)
        except:
            Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def create_device(sender, instance, created, **kwargs):
    if not created and instance.is_active is True:
        try:
            Device.objects.get_object_or_404(user=instance)
        except:
            Device.objects.create(user=instance)
