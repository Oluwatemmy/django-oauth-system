from .models import User
from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed


class UserRegisterSerializer(serializers.ModelSerializer):
    password=serializers.CharField(min_length=8, max_length=70, write_only=True)
    confirm_password=serializers.CharField(min_length=8, max_length=70, write_only=True)

    class Meta:
        model=User
        fields=["email", "first_name", "last_name", "password", "confirm_password"]

    def validate(self, attrs):
        password = attrs.get("password", "")
        confirm_password = attrs.get("confirm_password", "")

        if password != confirm_password:
            raise serializers.ValidationError("Passwords do not match")
        
        return attrs
    
    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data["email"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            password=validated_data["password"],
        )

        return user


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(min_length=8, max_length=255)
    password = serializers.CharField(min_length=8, max_length=70, write_only=True)
    full_name = serializers.CharField(max_length=255, read_only=True)
    access_token = serializers.CharField(max_length=255, read_only=True)
    refresh_token = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = User
        fields = ["email", "password", "full_name", "access_token", "refresh_token"]

    def validate(self, attrs):
        email = attrs.get("email", "")
        password = attrs.get("password", "")
        request = self.context.get('request')
        user = authenticate(request=request, email=email, password=password)

        if not user:
            raise AuthenticationFailed("Invalid email or password. Please try again")
        
        if not user.is_verified:
            raise AuthenticationFailed("Your account is not verified. Please verify your email address")
        token = user.tokens()

        return {
            'email': user.email,
            'full_name': user.get_full_name,
            'access_token': token['access'],
            'refresh_token': token['refresh']
        }






