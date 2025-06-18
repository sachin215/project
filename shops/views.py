from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import User_details
from rest_framework.permissions import AllowAny
from .serializers import UserCreateSerializer, UserProfileSerializer, UserUpdateSerializer
# Create your views here.
def home_page(request):
    return render(request, 'home.html')

class UserCreateView(APIView):

    # permission_classes = [AllowAny] # Allow any user to access this view
    def post(self, request):
        serializer = UserCreateSerializer(data=request.data,context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({"User":serializer.data,"message": "User created successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserListView(APIView):
    # permission_classes = [AllowAny] # Allow any user to access this view
    def get(self, request):
        users = User.objects.all()
        serializer = UserCreateSerializer(users, many=True,context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class UserUpdateView(APIView):
    def get(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = UserUpdateSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    # permission_classes = [AllowAny] # Allow any user to access this view
    def put(self, request, pk): 
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = UserUpdateSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User updated successfully"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserDetailView(APIView):
    # permission_classes = [AllowAny] # Allow any user to access this view
    def get(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = UserCreateSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
class UserDeleteView(APIView):
    # permission_classes = [AllowAny] # Allow any user to access this view
    def get(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = UserCreateSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    def delete(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
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
    # permission_classes = [AllowAny] # Allow any user to access this view
    def get(self, request, pk):
        try:
            user_details = User_details.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = UserProfileSerializer(user_details)
       
        return Response({"profile": serializer.data, "user":user_details.pk}, status=status.HTTP_200_OK)
    

class UserProfile_listView(APIView):
    # permission_classes = [AllowAny] # Allow any user to access this view
    def get(self, request):
        user_details = User_details.objects.all()
        serializer = UserProfileSerializer(user_details, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)