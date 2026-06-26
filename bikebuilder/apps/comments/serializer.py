from .models import Comments
from apps.users.serializer import UserPublicSerializer
from rest_framework import serializers

class CommentsSerializer(serializers.ModelSerializer):
    user = UserPublicSerializer(read_only=True)
    vote_count = serializers.SerializerMethodField()
    my_vote = serializers.SerializerMethodField()

    class Meta:
        model = Comments
        fields = ["id", "build", "user", "comment", "role", "vote_count", "my_vote", "created_at", "updated_at"]
        read_only_fields = ["id", "user", "role", "vote_count", "my_vote", "created_at", "updated_at"]

    def get_vote_count(self, obj):
        return obj.votes.count()

    def get_my_vote(self, obj):
        request = self.context.get("request")
        if not request or not request.user.is_authenticated:
            return False
        return obj.votes.filter(user=request.user).exists()
