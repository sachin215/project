from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from shops.models import User_details

@receiver(post_save, sender=User)
def create_user_details(sender, instance, created, **kwargs):
    if created:
        User_details.objects.create(user=instance)
    else:
        if User_details.objects.filter(user=instance).exists():
            pass
            # user_details = User_details.objects.get(user=instance)
            # user_details.save()

        else:
            User_details.objects.create(user=instance)