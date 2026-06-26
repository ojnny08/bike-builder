from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from apps.users.models import User


class Vote(models.Model):
    class Value(models.IntegerChoices):
        UP = 1, "Upvote"
        DOWN = -1, "Downvote"

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    value = models.SmallIntegerField(choices=Value.choices)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    target = GenericForeignKey("content_type", "object_id")

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "content_type", "object_id"],
                name="unique_user_vote",
            )
        ]
        indexes = [models.Index(fields=["content_type", "object_id"])]
