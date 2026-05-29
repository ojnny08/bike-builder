from django.db import models
from apps.category.models import BikeType, Component
from apps.users.models import User

# Create your models here.

class Build(models.Model):
    class Status(models.TextChoices):
        IN_PROGRESS = 'in_progress', 'In Progress'
        COMPLETE = 'complete', 'Complete'
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bikeType = models.ForeignKey(BikeType, on_delete=models.CASCADE)
    components = models.ManyToManyField(Component, blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.IN_PROGRESS)
    created_at = models.DateTimeField(auto_created=True)
    updated_at = models.DateTimeField(auto_now=True)
