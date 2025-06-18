from django.contrib import admin
from .models import Vendor, Document
# Register your models here.


admin.site.register(Document)

class VendorAdmin(admin.ModelAdmin):
    list_display = ('Vendor_name', 'is_approved', 'created_at', 'updated_at', 'Profile', 'user')
    list_display_links = ('Vendor_name', 'Profile', 'user')

admin.site.register(Vendor, VendorAdmin)
