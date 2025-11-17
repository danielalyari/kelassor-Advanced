from rest_framework import serializers
from .models import CustomUser, UserProfile, EmailVerification
import re


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['phone_number', 'profile_picture',
                  'birth_date', 'bio', 'linkedin', 'github']


class EmailVerificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailVerification
        fields = ['user', 'verification_code', 'is_verified', 'created_at']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'first_name',
                  'last_name', 'birth_date', 'phone_number']

    def validate_email(self, value):
        if not re.match(r"[^@]+@[^@]+\.[^@]+", value):
            raise serializers.ValidationError("ایمیل نامعتبر است.")
        return value

    def validate_phone_number(self, value):
        if not re.match(r"^\+?1?\d{9,15}$", value):
            raise serializers.ValidationError("شماره تلفن نامعتبر است.")
        return value
