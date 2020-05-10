from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save


class CustomUser(AbstractUser):
    pass


class Word(models.Model):
    word = models.CharField(max_length = 100, blank = True, null = True, unique = True)

    def __str__(self):
        return self.word

class Profile(models.Model):
    user = models.ForeignKey(
        get_user_model(),
        on_delete = models.CASCADE,
    )
    history = models.ForeignKey(
        Word,
        on_delete = models.CASCADE,
        related_name = 'history'
    ) 

    local_history = models.ForeignKey(
        Word,
        on_delete = models.CASCADE,
        related_name = 'local_history'
    ) 

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_profile_for_new_user(sender, created, instance, **kwargs):
    if created:
        profile = Profile(user_id=instance.id)
        profile.save()
