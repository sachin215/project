from django.http import response
from  rest_framework import permissions 

class VendorPermision(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_superuser or request.user.is_staff:
            return True
        else:
            return False
    
class IsReviewUserOrReadOnly1(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS and request.user.is_superuser:
            return True
        else:
            return obj.user == request.user or request.user.is_superuser
    


class IsCustomeronly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS and request.user.is_superuser:
            return True
        else:
            return request.user == obj or request.user.is_superuser
    