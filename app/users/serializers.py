from rest_framework import serializers
from .models import UserProfile

class UserProfileSerializer(serializers.Serializer):

    name = serializers.CharField(max_length=32)
    fam = serializers.CharField(max_length=32)
    otc = serializers.CharField(max_length=32)
    phone = serializers.CharField(max_length=32)
    email = serializers.EmailField()
    