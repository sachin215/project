from django.db import models
from django.contrib.auth.models import User as user
from shops.models import User_details
# Create your models here.
class Vendor(models.Model):
    user = models.OneToOneField(user, on_delete=models.CASCADE, related_name='vendor_profile')
    Profile = models.OneToOneField(User_details, on_delete=models.CASCADE, related_name='vendor_details')
    Vendor_name = models.CharField(max_length=100, unique=True)
    Vendor_description = models.TextField(null=True, blank=True)
    vendor_Licence = models.ImageField(upload_to='vendor_licences/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return self.Vendor_name
