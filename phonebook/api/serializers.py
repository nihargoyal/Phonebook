from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Contact, Profile

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = "__all__"

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['user', 'phone_number']

class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = User
        fields = ['id', 'username', 'profile']

class SearchSerializer(serializers.Serializer):
    name = serializers.CharField(required=False)
    phone_number = serializers.CharField(required=False)

class RegistrationSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField()

    def validate_phone_number(self, value):
        if len(value) < 10:
            raise serializers.ValidationError("Phone number should be at least 10 characters long.")
        return value

    class Meta:
        model = User
        fields = ['username', 'password', 'phone_number', 'first_name', 'last_name', 'email']
