from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = "categories"
        ordering = ["name"]

    def __str__(self):
        return self.name


class BikeType(models.Model):
    class Slug(models.TextChoices):
        ROAD = "road", "Road"
        MOUNTAIN = "mountain", "Mountain"
        GRAVEL = "gravel", "Gravel"
        FIXED = "fixed", "Fixed Gear"

    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True, choices=Slug.choices)

    def __str__(self):
        return self.name


class BikeTypeComponentRule(models.Model):
    class ComponentType(models.TextChoices):
        FRAME = "frame", "Frame"
        FORK = "fork", "Fork"
        BOTTOM_BRACKET = "bottom_bracket", "Bottom Bracket"
        CRANKSET = "crankset", "Crankset"
        CASSETTE = "cassette", "Cassette"
        REAR_DERAILLEUR = "rear_derailleur", "Rear Derailleur"
        FRONT_DERAILLEUR = "front_derailleur", "Front Derailleur"
        WHEEL = "wheel", "Wheel"
        TIRE = "tire", "Tire"
        HANDLEBAR = "handlebar", "Handlebar"
        STEM = "stem", "Stem"
        BRAKE = "brake", "Brake"
        SADDLE = "saddle", "Saddle"
        SEATPOST = "seatpost", "Seatpost"

    bike_type = models.ForeignKey(BikeType, on_delete=models.CASCADE, related_name="component_rules")
    component_type = models.CharField(max_length=30, choices=ComponentType.choices)
    required = models.BooleanField()

    class Meta:
        unique_together = ("bike_type", "component_type")

    def __str__(self):
        status = "required" if self.required else "optional"
        return f"{self.bike_type} — {self.get_component_type_display()} ({status})"


