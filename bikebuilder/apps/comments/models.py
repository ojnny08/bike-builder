from django.db import models
from django.core.validators import MaxLengthValidator
from django.contrib.contenttypes.fields import GenericRelation
from apps.users.models import User
from apps.builds.models import Build
from apps.vote.models import Vote


class Comments(models.Model):
    class Role(models.TextChoices):
        POSTER = "poster", "Poster"
        COMMENTER = "commenter", "Commenter"

    build = models.ForeignKey(Build, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField(validators=[MaxLengthValidator(1000)])
    role = models.CharField(max_length=10, choices=Role.choices)
    votes = GenericRelation(Vote)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
