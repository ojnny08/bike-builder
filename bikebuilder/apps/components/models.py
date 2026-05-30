from django.db import models
from ..category.models import Category, BikeType, BikeTypeComponentRule
# Create your models here.

class Components(models.Model):
    category = models.Model(Category, on_delete=models.CASCADE)
    bike_type = models.Model(BikeType, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    brand = models.CharField(max_length=20)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    weight_grams = models.PositiveIntegerField(help_text="Weight in grams")
    description = models.TextField(blank=True)
    image_url = models.URLField(blank=True)
    affiliate_url = models.URLField(blank=True)
    in_stock = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['brand', 'name']
    
    def __str__(self):
        return f"{self.brand} {self.name}"
    

class Frame(Components):
    class Material(models.TextChoices):
        CARBON = 'carbon', 'Carbon'
        ALUMINIUM = 'aluminium', 'Aluminium'
        STEEL = 'steel', 'Steel'

    class HeadTube(models.TextChoices):
        STRAIGHT = 'stright', 'Stright'
        TAPERED = 'tapered', 'Tapered'
    
    class BBShell(models.TextChoices):
        THREADED = "threaded", "Threaded (BSA)"
        PRESS_FIT = "press_fit", "Press Fit"
        T47 = "t47", "T47"
        BB30 = "bb30", "BB30"

    class RearAxleFit(models.TextChoices):
        TRACK = 'track_120', 'Track 120mm' 
        QR_130 = 'qr_130', 'Quick Release 130mm' # older road/fixed 
        QR_135 = 'qr_135', 'Quick Release 135mm'
        THRU_142 = 'thru_142', 'Thru Axle 142mm'
        TRU_142 = 'thur_148', 'Thru Axle 148mm'