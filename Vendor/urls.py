from django.urls import path
from django.contrib.auth import logout
from .views import VendorListView,Vendor_LogView, VendorLogoutView , VendorDetailView
urlpatterns = [
    path('vendors/', VendorListView.as_view(), name='vendor-list'),
    path('vendors/login/', Vendor_LogView.as_view(), name='vendor-login'),
    path('vendors/logout/', VendorLogoutView.as_view(), name='vendor-logout'),
    path('vendors/<int:pk>/', VendorDetailView.as_view(), name='vendor-detail')
]