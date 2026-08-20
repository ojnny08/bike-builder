from .models import Comments
from apps.users.serializer import UserPublicSerializer
from rest_framework import serializers

class CommentsSerializer(serializers.ModelSerializer):
    user = UserPublicSerializer(read_only=True)

    class Meta:
        model = Comments
        fields = ["id", "build", "user", "comment", "role", "created_at", "updated_at"]
        read_only_fields = ["id", "user", "role", "created_at", "updated_at"]
