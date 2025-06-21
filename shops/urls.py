from django.urls import path
from shops.views import home_page

from shops.views import UserCreateView, UserListView, UserUpdateView, UserDetailView, UserDeleteView, UserProfileView,UserProfile_listView

from django.urls import path

urlpatterns = [
    path('', home_page, name='home'),
       path('api/users/', UserListView.as_view(), name='user-list'),
    path('api/users/create/', UserCreateView.as_view(), name='user-create'),
    path('api/users/<int:pk>/update/', UserUpdateView.as_view(), name='user-update'),
    path('api/users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('api/users/<int:pk>/delete/', UserDeleteView.as_view(), name='user-delete'),
    path('api/users/<int:pk>/profile/', UserProfileView.as_view(), name='user-profile'),
    path('api/users/profile/', UserProfile_listView.as_view(), name='user-profile-list'),



]