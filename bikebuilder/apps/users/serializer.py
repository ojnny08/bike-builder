from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "firebase_uid", "email", "display_name", "photo_url", "role", "created_at"]
        read_only_fields = ["id", "firebase_uid", "created_at", "email", "role"]

class UserPublicSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "display_name", "photo_url"]