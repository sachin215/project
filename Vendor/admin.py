from django.contrib import admin
from .models import Vendor
# Register your models here.




class VendorAdmin(admin.ModelAdmin):
    list_display = ('Vendor_name', 'is_approved', 'created_at', 'updated_at', 'Profile', 'user')
    list_display_links = ('Vendor_name', 'Profile', 'user')

admin.site.register(Vendor, VendorAdmin)
