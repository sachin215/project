from django.shortcuts import render
from rest_framework.response import Response 
from .models import Vendor
from .serializers import VendorSerializer
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.parsers import JSONParser
from rest_framework import status,generics
from rest_framework.authtoken.views import obtain_auth_token
from shops.models import User
from django.contrib.auth import authenticate, login,logout
from rest_framework.decorators import api_view
from  .permision import VendorPermision,IsReviewUserOrReadOnly1
# Create your views here.

class VendorListView(generics.ListCreateAPIView):
    permission_classes = [VendorPermision]
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    parser_classes = [MultiPartParser, FormParser]
    def get(self, request):
        vendors = Vendor.objects.all()
        serializer = VendorSerializer(vendors, many=True, context={'request': request})
        if not vendors:
            return Response({'message': 'No vendors found'}, status=status.HTTP_404_NOT_FOUND)
        return Response({'vendors': serializer.data})
    def post(self, request):
        serializer = VendorSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Vendor created successfully'}, status=status.HTTP_201_CREATED)
        return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class Vendor_LogView(APIView):
    permission_classes = [VendorPermision]
    parser_classes = [JSONParser, MultiPartParser, FormParser]
    def get(self, request):
        logout_url = request.build_absolute_uri('/vendor/vendors/logout/')
        if request.user.is_authenticated:
            user = request.user
            vendor = Vendor.objects.filter(user=user).first()
            if vendor:
                return Response({'message': 'User is already logged in as a vendor', 'vendor_details': VendorSerializer(vendor, context={'request': request}).data, "logout_link": logout_url}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'User is need logged in'}, status=status.HTTP_403_FORBIDDEN)
        return Response({'error': 'User is not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        logout_url = request.build_absolute_uri('/vendor/vendors/logout/')
        if not username or not password:

            return Response({'error': 'Username and password are required'}, status=status.HTTP_400_BAD_REQUEST)
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            
            vendor = Vendor.objects.filter(user=user).first()
            if not vendor:
                return Response({'error': 'User is not a vendor'}, status=status.HTTP_403_FORBIDDEN)
            
            # Optionally, you can return a token or user details here
            return Response({'message': 'Login successful', 'user_username': user.username, 'Vendor_details': VendorSerializer(vendor,context={'request': request}).data, "logout_link": logout_url}, status=status.HTTP_200_OK)

        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class VendorLogoutView(APIView):        
    def get(self, request):
        logout(request)
        return Response({'message': 'Logged out successfully'}, status=status.HTTP_200_OK)
    

class VendorDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    permission_classes = [IsReviewUserOrReadOnly1]
    parser_classes = [MultiPartParser, FormParser]

