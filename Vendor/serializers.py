from rest_framework import serializers
from .models import Vendor ,Document
from  shops.models import User_details
from shops.serializers import UserCreateSerializer
class VendorSerializer(serializers.ModelSerializer):
    user=serializers.JSONField(write_only=True, required=True)
    Profile = serializers.HyperlinkedRelatedField(
        view_name='user-profile',
        read_only=True,  # This will link to the UserProfileSerializer view
    )
    class Meta:
        model = Vendor
        fields = [
            'Vendor_name',
            'Vendor_description',
            'vendor_Licence',
            'user',
            'Profile'   
        ]
        extra_kwargs = {
            'Vendor_name': {'required': True, 'max_length': 100},
            'Vendor_description': {'required': False, 'allow_blank': True},
            'vendor_Licence': {'required': False, 'allow_null': True},
        }
    def validate_Vendor_name(self, value):
        if Vendor.objects.filter(Vendor_name=value).exists():
            raise serializers.ValidationError("Vendor name already exists")
        return value
    
    def create(self, validated_data):
        print("Creating vendor profile with data:", validated_data)
        User_data= validated_data.pop('user', None)
        User_data['Role'] = 0
        if User_data:
            user = UserCreateSerializer(data=User_data, context=self.context)
            if user.is_valid():
                user.save()
                user_profile = User_details.objects.get(user=user.instance)
                vendor = Vendor.objects.create(user=user.instance, Profile=user_profile, **validated_data)
                return vendor
            else:
                raise serializers.ValidationError(user.errors)  
        else:
            raise serializers.ValidationError("User data is required to create a vendor profile")
        


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ['document_name', 'document_file', 'document_type']
        extra_kwargs = {
            'document_name': {'required': True, 'max_length': 100},
            'document_file': {'required': True},
            'document_type': {'required': True, 'max_length': 50},
        }
    
    def validate_document_name(self, value):
        if Document.objects.filter(document_name=value).exists():
            raise serializers.ValidationError("Document name already exists")
        return value