from django.db import models
from apps.category.models import BikeType
from apps.components.models import Components
from apps.users.models import User

# Create your models here.

class Build(models.Model):
    class Status(models.TextChoices):
        IN_PROGRESS = 'in_progress', 'In Progress'
        COMPLETE = 'complete', 'Complete'
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bikeType = models.ForeignKey(BikeType, on_delete=models.CASCADE)
    components = models.ManyToManyField(Components, blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.IN_PROGRESS)
    created_at = models.DateTimeField(auto_created=True)
    updated_at = models.DateTimeField(auto_now=True)
