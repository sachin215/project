from django.contrib import admin
from .models import User_details
@admin.register(User_details)
class UserDetailsAdmin(admin.ModelAdmin):
    list_display = ('user', 'Role', 'phone_number', 'address', 'city', 'pincode')
    search_fields = ('user__username', 'phone_number', 'city')
    list_filter = ('Role',)
# Register your models here.

