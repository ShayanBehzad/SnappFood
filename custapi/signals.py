from django.db.models.signals import post_save
from django.dispatch import receiver
# from django.contrib.auth.models import User
from register.models import User
from rest_framework.authtoken.models import Token

@receiver(post_save, sender=User, weak=False)
def tokencreate(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)