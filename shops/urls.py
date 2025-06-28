from django.urls import path
from shops.views import home_page

from shops.views import UserCreateView, UserListView, UserUpdateView, UserDetailView, UserDeleteView, \
UserProfileView,UserProfile_listView, Login_view,Dashboard,LogoutView,Signup,user_login,user_Profile

from django.contrib.auth import views as auth_views
from django.urls import path

urlpatterns = [
    path('', home_page, name='home'),
       path('api/users/', UserListView.as_view(), name='user-list'),
    path('users/create/', UserCreateView.as_view(), name='user-create'),
    path('api/users/<int:pk>/update/', UserUpdateView.as_view(), name='user-update'),
    path('api/users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('api/users/<int:pk>/delete/', UserDeleteView.as_view(), name='user-delete'),
    path('api/users/<int:pk>/profile/', UserProfileView.as_view(), name='user-profile'),
    path('api/users/profile/', UserProfile_listView.as_view(), name='user-profile-list'),
    path('api/users/login/', Login_view.as_view(), name='user-login'),
    path('user/logout/', LogoutView.as_view(), name='user-logout'),
    path('Dashboard/',Dashboard,name='Dashboard'),
    path('Signup/',Signup,name='Signup'),
    path('login/',user_login,name='login'),
    path('profile/',user_Profile,name='profile')
    
    
]

