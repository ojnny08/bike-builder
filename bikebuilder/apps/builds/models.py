import secrets

from django.db import models
from apps.category.models import BikeType
from apps.components.models import Components
from apps.users.models import User

# Create your models here.

def generate_share_token():
    return secrets.token_urlsafe(9)[:12]

class Build(models.Model):
    class Status(models.TextChoices):
        IN_PROGRESS = 'in_progress', 'In Progress'
        COMPLETE = 'complete', 'Complete'
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=40, default="New Build")
    bikeType = models.ForeignKey(BikeType, on_delete=models.CASCADE)
    components = models.ManyToManyField(Components, blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.IN_PROGRESS)
    image_url = models.URLField(blank=True)
    share_token = models.CharField(max_length=12, unique=True, db_index=True, default=generate_share_token, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
