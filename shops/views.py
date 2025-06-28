from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import User_details
from rest_framework.permissions import AllowAny
from .serializers import UserCreateSerializer, UserProfileSerializer, UserUpdateSerializer
from Vendor import permision
from rest_framework import generics
from  Vendor.permision import VendorPermision
from django.contrib.auth import authenticate, login,logout
from django.http import HttpResponse
# Create your views here.
def home_page(request):
    return render(request, 'home.html')



class UserCreateView(generics.CreateAPIView):
    serializer_class=UserCreateSerializer
    def post(self, request):
        serializer = UserCreateSerializer(data=request.data,context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({"User":serializer.data,"message": "User created successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserListView(APIView):
    permission_classes = [permision.IsCustomeronly]
    def get(self, request):
        users = User.objects.all()
        self.check_object_permissions(request,users)
        serializer = UserCreateSerializer(users, many=True,context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class UserUpdateView(APIView):
    permission_classes = [permision.IsCustomeronly]
    def get(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
            self.check_object_permissions(request,user)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = UserUpdateSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    # permission_classes = [AllowAny] # Allow any user to access this view
    def put(self, request, pk): 
        try:
            user = User.objects.get(pk=pk)
            self.check_object_permissions(request,user)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = UserUpdateSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User updated successfully"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserDetailView(APIView):
    permission_classes = [permision.IsCustomeronly]
    def get(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
            self.check_object_permissions(request,user)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = UserCreateSerializer(user,context={'request': request})
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class UserDeleteView(APIView):
    permission_classes = [permision.IsCustomeronly]
    def get(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
            self.check_object_permissions(request,user)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = UserCreateSerializer(user,context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    

    def delete(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
            self.check_object_permissions(request,user)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        user.delete()
        return Response({"message": "User deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    
# class UserForgotPasswordView(APIView):
#     # permission_classes = [AllowAny] # Allow any user to access this view
#     def post(self, request):
#         email = request.data.get('email')
#         try:
#             user = User.objects.get(email=email)
#         except User.DoesNotExist:
#             return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
#         # Send email logic here
#         Token.objects.get_or_create(user=user)
#         return Response({"message": "Token Generated successfully Please Contact Admin ,call 9731540114"}, status=status.HTTP_200_OK)

class UserProfileView(APIView):
    permission_classes = [permision.IsCustomeronly] # Allow any user to access this view
    def get(self, request, pk):
        try:
            user_details = User_details.objects.get(pk=pk)
            self.check_object_permissions(request,user_details)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = UserProfileSerializer(user_details)
        return Response({"profile": serializer.data}, status=status.HTTP_200_OK)

def user_Profile(request):
    if request.user.username !='':
        return render(request,'profile.html')
    else:
        return redirect('login') 


class UserProfile_listView(APIView):
    permission_classes=[permision.IsCustomeronly]
    def get(self, request):
        user_details = User_details.objects.all()
        self.check_object_permissions(request,user_details)
        serializer = UserProfileSerializer(user_details, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

# views.py
def Signup(request):
    return render(request,'signup.html')

def user_login(request):
    return render(request,'login.html')

def Dashboard(request):
    if request.user.username !='':
        data = request.session.get('logout',None)  # safer than direct access
        return render(request, 'Dashboard.html', context=data)
    else:
        return redirect('login') 
    

class Login_view(APIView):
    def get(self,request):
        return redirect('login')
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        logout_url = request.build_absolute_uri('/shop/user/logout/')
        if not username or not password:
            return Response({'error': 'Username and password are required'}, status=status.HTTP_400_BAD_REQUEST)
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            request.session['logout']={'logout': logout_url}
            return Response({'logout': logout_url, 'user': user.username},status=status.HTTP_200_OK )
            # return redirect('Dashboard')  # make sure 'Dashboard' exists in your urls.py
        else:
            return Response({'message': 'Invalid credentials'},status=status.HTTP_400_BAD_REQUEST)

class LogoutView(APIView):
    def get(self, request):
        logout(request)
        return redirect('login')