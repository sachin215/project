from django.urls import path


from .views import VendorListView,DocumentListView
urlpatterns = [
    path('vendors/', VendorListView.as_view(), name='vendor-list'),
    path('documents/', DocumentListView.as_view(), name='document-list')
]