from django.dispatch import receiver
from django.db.models.signals import post_save
from rest_framework import serializers

from django.contrib.auth.models import User
from shops.models import User_details
from .models import User_details
class UserCreateSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True)
    profile=serializers.HyperlinkedRelatedField(
        view_name='user-profile',
        read_only=True, # This will link to the UserProfileSerializer view
        

    )
    Role = serializers.IntegerField(
        
        write_only=True,
        required=False,
    
    )
    class Meta:
        model = User
        fields = [  # This will include all fields from the User model
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'password',
            'password2',
            'profile',
            'Role'
           
        ]
        extra_kwargs = {
            'password': {'write_only': True, 'required': True},
            'email': {'required': True, },
            'username': {'required': True},
            'password2': {'write_only': True, 'required': True,},
            'first_name': {'required': True},
            'last_name': {'required': True},
           
        }


    def validate(self, data):
        
        if data['password'] != data.pop('password2',None):
            raise serializers.ValidationError("Passwords do not match")
        return data
    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already exists")
        return value
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists")
        return value
    
    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long")
        if not any(char.isdigit() for char in value):
            raise serializers.ValidationError("Password must contain at least one digit")
        if not any(char.isalpha() for char in value):
            raise serializers.ValidationError("Password must contain at least one letter")
        return value
      
    def create(self, validated_data):
        Role= validated_data.pop('Role', None)
        user = User(**validated_data)
        # Hash the password before saving

        user.set_password(validated_data['password'])
        user.save()
    
        User_details.objects.filter(user=user).update(
            Role=Role
        )
        return user
    def update(self, instance, validated_data):
        pass
    

class UserUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name','password',]
        extra_kwargs = {
            'password': {'write_only': True}
        }
    
    def create(self, validated_data):
        pass
       
    def update(self, instance, validated_data):
        
        # Check if the password is correct
        if not instance.check_password(validated_data.get('password')):
            raise serializers.ValidationError("Incorrect password")
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.save()
        return instance

class UserchangePasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['password']
        extra_kwargs = {
            'password': {'write_only': True}
        }
    
    def update(self, instance, validated_data):
        if not instance.check_password(validated_data.get('old_password')):
            raise serializers.ValidationError("Incorrect password")
        # Check if the new password is the same as the old password
        if instance.check_password(validated_data.get('password')):
            raise serializers.ValidationError("New password cannot be the same as the old password")
        # Hash the new password before saving
        instance.set_password(validated_data['password'])
        instance.save()
        return instance
    


class UserProfileSerializer(serializers.ModelSerializer):
    role=serializers.CharField(source='get_Role_display', read_only=True)  # This will return the display value of the role field
    username=serializers.CharField(source='user.username',read_only=True)

    class Meta:
        model = User_details
        fields = ['username','phone_number', 'address', 'city', 'pincode', 'profile_picture', 'cover_picture', 'role']  # This will include all fields from the User_details model

    def create(self, validated_data):
        user_details = User_details(**validated_data)
        user_details.save()
        return user_details

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance