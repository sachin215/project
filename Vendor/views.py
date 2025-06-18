from django.shortcuts import render
from rest_framework.response import Response 
from .models import Vendor, Document
from .serializers import VendorSerializer ,DocumentSerializer
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.parsers import JSONParser
from rest_framework import status,mixins,generics


# Create your views here.

class VendorListView(generics.ListCreateAPIView):
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
    
class DocumentListView(generics.ListCreateAPIView):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    parser_classes = [MultiPartParser, FormParser]
    def get(self, request):
        documents = Document.objects.all()
        serializer = DocumentSerializer(documents, many=True, context={'request': request})
        if not documents:
            return Response({'message': 'No documents found'}, status=status.HTTP_404_NOT_FOUND)
        return Response({'documents': serializer.data})
    def post(self, request):
        serializer = DocumentSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Document created successfully'}, status=status.HTTP_201_CREATED)
        return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
