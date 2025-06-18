
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver



class User_details(models.Model):
    Rastorant=0
    Customer=1
    admin=2
    USER_TYPE_CHOICES = [
        (0, 'Restaurant'),
        (1, 'Customer'),
        (2, 'Administrator'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    Role = models.IntegerField(choices=USER_TYPE_CHOICES, default=1)  # Default to Customer
    phone_number = models.CharField(max_length=15, unique=True, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    pincode = models.CharField(max_length=10, null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    cover_picture = models.ImageField(upload_to='cover_pictures/', null=True, blank=True)

    def __str__(self):
        return f"{self.user.email}"
    
# @receiver(post_save, sender=User)
# def create_user_details(sender, instance, created, **kwargs):
#     if created:
#         User_details.objects.create(user=instance)
#     else:
#         if User_details.objects.filter(user=instance).exists():
#             pass
#             # user_details = User_details.objects.get(user=instance)
#             # user_details.save()

#         else:
#             User_details.objects.create(user=instance)
        
  