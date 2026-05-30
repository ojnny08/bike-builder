from django.db import models

class BikeType(models.Model):
      class Slug(models.TextChoices):
          ROAD    = "road",     "Road"
          MOUNTAIN = "mountain", "Mountain"
          GRAVEL  = "gravel",   "Gravel"
          FIXED   = "fixed",    "Fixed Gear"

      RULES = {
          "road": {
              "required": ["frame", "fork", "crankset", "cassette", "rear_derailleur", "wheel", "tire", "handlebar", "stem", "brake", "saddle",
  "seatpost"],
              "optional": ["front_derailleur"],
          },
          "mountain": {
              "required": ["frame", "fork", "crankset", "cassette", "rear_derailleur", "wheel", "tire", "handlebar", "stem", "brake", "saddle",
  "seatpost"],
              "optional": ["front_derailleur"],
          },
          "gravel": {
              "required": ["frame", "fork", "crankset", "cassette", "rear_derailleur", "wheel", "tire", "handlebar", "stem", "brake", "saddle",
  "seatpost"],
              "optional": ["front_derailleur"],
          },
          "fixed": {
              "required": ["frame", "fork", "crankset", "wheel", "tire", "handlebar", "stem", "saddle", "seatpost"],
              "optional": ["brake"],
          },
      }

      name = models.CharField(max_length=50)
      slug = models.SlugField(choices=Slug.choices)

      def get_rules(self):
          return self.RULES.get(self.slug, {"required": [], "optional": []})





